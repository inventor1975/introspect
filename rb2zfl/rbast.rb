# rbast — thin Ruby AST -> JSON dumper for rb2zfl (the introspect's Ruby module).
# Uses Ruby's OWN Ripper (stdlib, zero install). Normalizes Ripper's verbose sexp into the SAME compact
# schema the other modules use (call/member/ident/lit/bin/aref/template/assign/if/return/...), collecting
# every def/defs into a flat `funcs` list (+ a synthetic "<top>"). Usage: ruby rbast.rb <file.rb>
require 'ripper'
require 'json'

$funcs = []
$owner = []          # the enclosing class/module names

def leaf_line(n)
  (n.is_a?(Array) && n[2].is_a?(Array)) ? n[2][0] : 0
end

def ident_name(n)
  return nil unless n.is_a?(Array)
  return n[1] if n[0].to_s.start_with?("@")
  return ident_name(n[1]) if %w[var_ref var_field vcall fcall const_ref].include?(n[0].to_s)
  nil
end

def call_line(n)
  return 0 unless n.is_a?(Array)
  return leaf_line(n) if n[0].to_s.start_with?("@")
  n.each { |c| l = call_line(c); return l if l > 0 }
  0
end

# gather string_embexpr interpolations (#{...}) into `out` as encoded expressions
def collect_embexpr(n, out)
  return unless n.is_a?(Array)
  if n[0].to_s == "string_embexpr"
    (n[1] || []).each { |s| out << enc(s) }
    return
  end
  n.each { |c| collect_embexpr(c, out) if c.is_a?(Array) }
end

# Ripper hands the SOURCE text of a literal: \" is still two characters; the value has one
def unesc(s)
  s.to_s.gsub(/\\(["'\\#])/, '\1')
end

# the same string as ordered parts: {"s" => literal text} / {"e" => expression}
def collect_parts(n, out)
  return unless n.is_a?(Array)
  t = n[0].to_s
  if t == "@tstring_content"
    out << { "s" => unesc(n[1]) }; return
  end
  if t == "string_embexpr"
    (n[1] || []).each { |s| out << { "e" => enc(s) } }
    return
  end
  n.each { |c| collect_parts(c, out) if c.is_a?(Array) }
end

def enc_string(n)
  exprs = []; collect_embexpr(n, exprs)
  parts = []; collect_parts(n, parts)
  return { "k" => "lit", "kind" => "STRING", "value" => parts.map { |p| p["s"] }.join } if exprs.empty?
  { "k" => "template", "exprs" => exprs, "parts" => parts }
end

# an if / unless / case used as a VALUE: its branches' statements
def cond_expr(test, branches)
  { "k" => "condexpr", "test" => test, "branches" => branches }
end

def else_branch(node)
  return [] unless node.is_a?(Array)
  return enc_stmts(node[1]) if node[0].to_s == "else"
  return [{ "k" => "exprstmt", "x" => enc(node), "line" => call_line(node) }] if node[0].to_s == "elsif"
  []
end

def enc_args(n)
  # arg_paren -> args_add_block -> [ [args...], block ]
  args = []
  walk = nil
  list = lambda do |l|                                   # a plain list of args, or a nested args node
    next unless l.is_a?(Array)
    if l[0].is_a?(Symbol) then walk.call(l) else l.each { |a| args << enc(a) } end
  end
  walk = lambda do |x|
    return unless x.is_a?(Array)
    if x[0].to_s == "args_add_block"
      list.call(x[1])
    elsif %w[arg_paren paren].include?(x[0].to_s)
      walk.call(x[1])
    elsif x[0].to_s == "args_add"
      walk.call(x[1]); args << enc(x[2])
    elsif x[0].to_s == "args_add_star"                   # f(a, *rest, b): the splat is an argument too
      list.call(x[1]); args << enc(x[2]); (x[3..] || []).each { |a| args << enc(a) }
    end
  end
  walk.call(n)
  args
end

def param_names(n)
  names = []
  return names unless n.is_a?(Array)
  p = (n[0].to_s == "paren") ? n[1] : n
  return names unless p.is_a?(Array) && p[0].to_s == "params"
  # p[1]=required, p[2]=optional [[name,default]...], p[3]=rest, ...
  (p[1] || []).each { |x| names << ident_name(x) } if p[1].is_a?(Array)
  (p[2] || []).each { |pair| names << ident_name(pair[0]) } if p[2].is_a?(Array)
  names << ident_name(p[3][1]) if p[3].is_a?(Array) && p[3][1]      # *rest
  names.compact
end

def add_func(name, params_node, body_node)
  $funcs << { "k" => "func", "name" => name || "", "params" => param_names(params_node),
              "owner" => $owner.last, "body" => enc_body(body_node) }
end

# bodystmt -> encoded statements; rescue / else / ensure become a "try" (they were dropped)
def enc_body(bodystmt)
  return enc_stmts(bodystmt) unless bodystmt.is_a?(Array) && bodystmt[0].to_s == "bodystmt"
  main = enc_stmts(bodystmt[1] || [])
  resc, elsp, ens = bodystmt[2], bodystmt[3], bodystmt[4]
  return main if resc.nil? && elsp.nil? && ens.nil?
  handler = []; pnames = []
  cur = resc
  while cur.is_a?(Array) && cur[0].to_s == "rescue"
    pnames << ident_name(cur[2]) if cur[2]
    handler += enc_stmts(cur[3] || [])
    cur = cur[4]
  end
  main += enc_stmts(elsp.is_a?(Array) && elsp[0].to_s == "else" ? elsp[1] : elsp) if elsp
  fin = (ens.is_a?(Array) && ens[0].to_s == "ensure") ? enc_stmts(ens[1] || []) : []
  [{ "k" => "try", "body" => main, "handler" => handler, "param" => pnames.compact, "finalizer" => fin }]
end

# the names a block / multiple-assignment binds
def mlhs_names(n)
  return [] unless n.is_a?(Array)
  nm = ident_name(n)
  return [nm] if nm
  n.flat_map { |c| c.is_a?(Array) ? mlhs_names(c) : [] }.uniq
end

def enc_block(b)
  return nil unless b.is_a?(Array)
  params = (b[1].is_a?(Array) && b[1][0].to_s == "block_var") ? param_names(b[1][1]) : []
  body = b[2]
  body = (body.is_a?(Array) && body[0].to_s == "bodystmt") ? enc_body(body) : enc_stmts(body)
  { "params" => params, "body" => body }
end

def body_of(bodystmt)
  # bodystmt -> [ "bodystmt", [stmts], rescue, else, ensure ]
  return [] unless bodystmt.is_a?(Array)
  return bodystmt[1] || [] if bodystmt[0].to_s == "bodystmt"
  bodystmt
end

def enc(n)
  return { "k" => "nil" } unless n.is_a?(Array)
  t = n[0].to_s
  case t
  when "@ident", "@const", "@ivar", "@gvar", "@cvar", "@kw"
    { "k" => "ident", "name" => n[1] }
  when "@int", "@float", "@CHAR"
    { "k" => "lit", "kind" => "NUM" }
  when "@tstring_content"
    { "k" => "lit", "kind" => "STRING", "value" => unesc(n[1]) }
  when "const_path_ref"                                   # File::SEPARATOR: base ident File, full name kept
    b = enc(n[1]); b = b.merge("full" => "#{b["full"] || b["name"]}::#{ident_name(n[2])}") if b["k"] == "ident"; b
  when "var_ref", "var_field", "vcall", "const_ref", "top_const_ref"
    enc(n[1])
  when "string_literal", "string_content", "string_concat"
    enc_string(n)
  when "regexp_literal"
    exprs = []; collect_embexpr(n, exprs)
    parts = []; collect_parts(n[1], parts)
    { "k" => "regex", "src" => parts.map { |p| p["s"] || "" }.join, "interp" => !exprs.empty?, "exprs" => exprs }
  when "begin"                                           # x = begin .. rescue .. nil end: a value with branches
    b = enc_body(n[1])
    if b.length == 1 && b[0]["k"] == "try"
      cond_expr({ "k" => "nil" }, [b[0]["body"], b[0]["handler"]])
    else
      cond_expr({ "k" => "nil" }, [b])
    end
  when "ifop"
    cond_expr(enc(n[1]), [[{ "k" => "exprstmt", "x" => enc(n[2]) }], [{ "k" => "exprstmt", "x" => enc(n[3]) }]])
  when "if", "elsif"
    cond_expr(enc(n[1]), [enc_stmts(n[2]), else_branch(n[3])])
  when "unless"
    cond_expr({ "k" => "unary", "op" => "!", "x" => enc(n[1]) }, [enc_stmts(n[2]), else_branch(n[3])])
  when "if_mod"
    cond_expr(enc(n[1]), [[enc_stmt(n[2])], []])
  when "unless_mod"
    cond_expr({ "k" => "unary", "op" => "!", "x" => enc(n[1]) }, [[enc_stmt(n[2])], []])
  when "case"
    br = []; cur = n[2]
    while cur.is_a?(Array) && %w[when in].include?(cur[0].to_s)
      br << enc_stmts(cur[2]); cur = cur[3]
    end
    br << (cur.is_a?(Array) && cur[0].to_s == "else" ? enc_stmts(cur[1]) : [])
    cond_expr(enc(n[1]), br)
  when "xstring_literal"      # `cmd` backticks (also %x{}) -> shell execution of the string
    exprs = []; collect_embexpr(n, exprs)
    { "k" => "xstring", "exprs" => exprs, "line" => call_line(n) }
  when "symbol_literal", "dyna_symbol", "symbol", "label"
    { "k" => "lit", "kind" => "SYM", "value" => (t == "symbol_literal" && n[1].is_a?(Array)) ? ident_name(n[1][1]) : nil }
  when "words_new", "qwords_new", "qwords_add", "words_add", "qwords_literal", "words_literal", "qsymbols_literal", "symbols_literal"
    elts = []
    walk = lambda { |x| next unless x.is_a?(Array); if x[0].to_s == "@tstring_content" then elts << { "k" => "lit", "kind" => "STRING", "value" => x[1] } else x.each { |c| walk.call(c) } end }
    walk.call(n)
    { "k" => "array", "elts" => elts }
  when "binary"
    { "k" => "bin", "op" => n[2].to_s, "x" => enc(n[1]), "y" => enc(n[3]) }
  when "unary"
    { "k" => "unary", "op" => n[1].to_s, "x" => enc(n[2]) }
  when "aref"
    { "k" => "aref", "object" => enc(n[1]), "index" => enc_args(n[2]), "line" => call_line(n[1]) }  # params[:x]
  when "method_add_arg"
    { "k" => "call", "callee" => enc(n[1]), "args" => enc_args(n[2]), "line" => call_line(n[1]) }
  when "method_add_block"                                 # x.each do |e| .. end: the block body is walked
    c = enc(n[1])
    c = { "k" => "call", "callee" => c, "args" => [], "line" => (c["line"] || call_line(n[1])) } if c["k"] != "call"
    c["block"] = enc_block(n[2])
    c
  when "mrhs_new_from_args", "mrhs_add", "mrhs_new", "mrhs_add_star"
    elts = []
    n[1..].each { |x| next unless x.is_a?(Array); (x[0].is_a?(Array) ? x : [x]).each { |e| elts << enc(e) if e.is_a?(Array) } }
    { "k" => "array", "elts" => elts }
  when "command"
    { "k" => "call", "callee" => enc(n[1]), "args" => enc_args(n[2]), "line" => call_line(n[1]) }
  when "command_call"
    { "k" => "call",
      "callee" => { "k" => "member", "object" => enc(n[1]), "prop" => ident_name(n[3]) },
      "args" => enc_args(n[4]), "line" => call_line(n[1]) }
  when "call"
    { "k" => "member", "object" => enc(n[1]), "prop" => ident_name(n[3]), "line" => call_line(n) }
  when "fcall"
    enc(n[1])
  when "aref_field"                                      # h[:k] = v: an index store
    { "k" => "aref", "object" => enc(n[1]) }
  when "field"
    { "k" => "member", "object" => enc(n[1]), "prop" => ident_name(n[3]) }
  when "array"
    elts = []; (n[1] || []).each { |e| elts << enc(e) } if n[1].is_a?(Array)
    { "k" => "array", "elts" => elts }
  when "hash", "bare_assoc_hash", "assoclist_from_args"
    vals = []; keys = []
    src = (t == "hash") ? (n[1].is_a?(Array) ? n[1][1] : nil) : n[1]  # hash -> assoclist -> [assocs]
    (src || []).each do |a|
      vals << enc(a)
      k = (a.is_a?(Array) && a[0].to_s == "assoc_new") ? a[1] : nil
      keys << ((k.is_a?(Array) && k[0].to_s == "@label") ? k[1].to_s.chomp(":") :
               (k.is_a?(Array) && k[0].to_s == "symbol_literal") ? ident_name(k[1].is_a?(Array) ? k[1][1] : nil) : nil)
    end if src.is_a?(Array)
    { "k" => "array", "hash" => true, "keys" => keys, "elts" => vals }  # VALUES kept for taint, keys for options
  when "assoc_new", "assoc_splat"
    enc(n[2] || n[1])                                                 # the value side of key: value
  when "paren"
    inner = n[1]
    inner = inner[0] if inner.is_a?(Array) && inner[0].is_a?(Array)
    enc(inner)
  when "assign"
    { "k" => "assignexpr", "left" => enc(n[1]), "right" => enc(n[2]) }
  else
    { "k" => "other", "t" => t }
  end
end

def enc_stmts(list)
  return [] unless list.is_a?(Array)
  list.map { |s| enc_stmt(s) }
end

def else_of(node)
  return nil unless node.is_a?(Array)
  return { "k" => "block", "body" => enc_stmts(node[1]) } if node[0].to_s == "else"
  return enc_stmt(node) if node[0].to_s == "elsif"
  nil
end

def enc_stmt(s)
  return { "k" => "other" } unless s.is_a?(Array)
  case s[0].to_s
  when "assign"
    { "k" => "assign", "left" => enc(s[1]), "right" => enc(s[2]), "line" => call_line(s[1]) }
  when "opassign"
    { "k" => "assign", "op" => s[2][1].to_s, "left" => enc(s[1]), "right" => enc(s[3]), "line" => call_line(s[1]) }
  when "massign"
    { "k" => "assign", "left" => { "k" => "other" }, "names" => mlhs_names(s[1]), "right" => enc(s[2]),
      "line" => call_line(s[1]) }
  when "if", "elsif"
    { "k" => "if", "test" => enc(s[1]), "body" => enc_stmts(s[2]), "els" => else_of(s[3]), "line" => call_line(s[1]) }
  when "unless"                                        # the negation is the whole point of `unless`
    { "k" => "if", "test" => { "k" => "unary", "op" => "!", "x" => enc(s[1]) }, "body" => enc_stmts(s[2]),
      "els" => else_of(s[3]), "line" => call_line(s[1]) }
  when "if_mod"
    { "k" => "if", "test" => enc(s[1]), "body" => [enc_stmt(s[2])], "els" => nil, "line" => call_line(s[1]) }
  when "unless_mod"
    { "k" => "if", "test" => { "k" => "unary", "op" => "!", "x" => enc(s[1]) }, "body" => [enc_stmt(s[2])],
      "els" => nil, "line" => call_line(s[1]) }
  when "next", "break", "redo", "retry"
    { "k" => "branch", "tok" => s[0].to_s, "line" => call_line(s) }
  when "for"                                           # for x in arr
    { "k" => "for", "left" => mlhs_names(s[1]), "iter" => enc(s[2]), "body" => enc_stmts(s[3]), "line" => 0 }
  when "while", "until", "while_mod", "until_mod"
    body = s[0].end_with?("_mod") ? [enc_stmt(s[2])] : enc_stmts(s[2])
    { "k" => "for", "test" => enc(s[1]), "body" => body, "line" => 0 }
  when "case"
    { "k" => "switch", "cases" => enc_cases(s[2]), "line" => 0 }
  when "return", "return0"
    { "k" => "return", "argument" => enc(s[1]), "line" => call_line(s) }
  when "def"
    add_func(ident_name(s[1]), s[2], s[3]); { "k" => "funcref" }
  when "defs"                                          # def self.name
    add_func(ident_name(s[3]), s[4], s[5]); { "k" => "funcref" }
  when "class", "module"
    enc_class(s); { "k" => "other" }
  when "begin"
    { "k" => "block", "body" => enc_body(s[1]) }
  when "void_stmt"
    { "k" => "other" }
  else
    { "k" => "exprstmt", "x" => enc(s), "line" => call_line(s) }
  end
end

def enc_cases(node)
  cases = []
  cur = node
  while cur.is_a?(Array) && %w[when in].include?(cur[0].to_s)
    cases << { "k" => "case", "body" => enc_stmts(cur[2]) }
    cur = cur[3]
  end
  cases << { "k" => "case", "isdefault" => true, "body" => enc_stmts(cur[1]) } if cur.is_a?(Array) && cur[0].to_s == "else"
  cases
end

# a class / module body: defs become functions; the rest of the body (Sinatra routes, before_action,
# constants) becomes a synthetic "<class Name>" function, so a route block in a Sinatra::Base is walked
def enc_class(node)
  name = ident_name(node[1]) || "?"
  $owner.push(name)
  body = node[0].to_s == "class" ? node[3] : node[2]
  stmts = body_of(body)
  rest = []
  (stmts || []).each do |st|
    next unless st.is_a?(Array)
    case st[0].to_s
    when "def" then add_func(ident_name(st[1]), st[2], st[3])
    when "defs" then add_func(ident_name(st[3]), st[4], st[5])
    when "class", "module" then enc_class(st)
    when "sclass" then collect_defs(st)
    else rest << enc_stmt(st)
    end
  end
  $funcs << { "k" => "func", "name" => "<class #{name}>", "params" => [], "owner" => name, "body" => rest } unless rest.empty?
  $owner.pop
end

def collect_defs(node)
  return unless node.is_a?(Array)
  if node[0].to_s == "def"
    add_func(ident_name(node[1]), node[2], node[3]); return
  elsif node[0].to_s == "defs"
    add_func(ident_name(node[3]), node[4], node[5]); return
  end
  node.each { |c| collect_defs(c) if c.is_a?(Array) }
end

begin
  src = File.read(ARGV[0])
  sexp = Ripper.sexp(src)
  if sexp.nil?
    print JSON.generate({ "k" => "file", "error" => "parse", "funcs" => [] }); exit 0
  end
  top = enc_stmts(sexp[1])                              # program -> [stmts]
  $funcs << { "k" => "func", "name" => "<top>", "params" => [], "body" => top }
  print JSON.generate({ "k" => "file", "funcs" => $funcs })
rescue => e
  print JSON.generate({ "k" => "file", "error" => e.to_s, "funcs" => [] })
end
