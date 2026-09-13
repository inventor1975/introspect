# rbast — thin Ruby AST -> JSON dumper for rb2zfl (the introspect's Ruby module).
# Uses Ruby's OWN Ripper (stdlib, zero install). Normalizes Ripper's verbose sexp into the SAME compact
# schema the other modules use (call/member/ident/lit/bin/aref/template/assign/if/return/...), collecting
# every def/defs into a flat `funcs` list (+ a synthetic "<top>"). Usage: ruby rbast.rb <file.rb>
require 'ripper'
require 'json'

$funcs = []

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

def enc_args(n)
  # arg_paren -> args_add_block -> [ [args...], block ]
  args = []
  walk = lambda do |x|
    return unless x.is_a?(Array)
    if x[0].to_s == "args_add_block"
      (x[1] || []).each { |a| args << enc(a) } if x[1].is_a?(Array)
    elsif %w[arg_paren paren].include?(x[0].to_s)
      walk.call(x[1])
    elsif x[0].to_s == "args_add"
      walk.call(x[1]); args << enc(x[2])
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
              "body" => enc_stmts(body_of(body_node)) }
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
    { "k" => "lit", "kind" => "STRING" }
  when "var_ref", "var_field", "vcall", "const_ref", "const_path_ref", "top_const_ref"
    enc(n[1])
  when "string_literal", "string_content"
    exprs = []; collect_embexpr(n, exprs)
    exprs.empty? ? { "k" => "lit", "kind" => "STRING" } : { "k" => "template", "exprs" => exprs }
  when "xstring_literal"      # `cmd` backticks (also %x{}) -> shell execution of the string
    exprs = []; collect_embexpr(n, exprs)
    { "k" => "xstring", "exprs" => exprs, "line" => call_line(n) }
  when "symbol_literal", "dyna_symbol", "symbol", "label"
    { "k" => "lit", "kind" => "SYM" }
  when "binary"
    { "k" => "bin", "op" => n[2].to_s, "x" => enc(n[1]), "y" => enc(n[3]) }
  when "unary"
    { "k" => "unary", "op" => n[1].to_s, "x" => enc(n[2]) }
  when "aref"
    { "k" => "aref", "object" => enc(n[1]) }             # params[:x] -> taint flows from object
  when "method_add_arg"
    { "k" => "call", "callee" => enc(n[1]), "args" => enc_args(n[2]), "line" => call_line(n[1]) }
  when "method_add_block"
    enc(n[1])                                             # ignore block body for slice-1 taint
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
  when "aref_field", "field"
    { "k" => "member", "object" => enc(n[1]), "prop" => ident_name(n[3]) }
  when "array"
    elts = []; (n[1] || []).each { |e| elts << enc(e) } if n[1].is_a?(Array)
    { "k" => "array", "elts" => elts }
  when "hash", "bare_assoc_hash", "assoclist_from_args"
    vals = []
    src = (t == "hash") ? (n[1].is_a?(Array) ? n[1][1] : nil) : n[1]  # hash -> assoclist -> [assocs]
    (src || []).each { |a| vals << enc(a) } if src.is_a?(Array)
    { "k" => "array", "elts" => vals }                                # preserve VALUES (nested calls) for taint
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
    { "k" => "assign", "left" => enc(s[1]), "right" => enc(s[3]), "line" => call_line(s[1]) }
  when "massign"
    { "k" => "assign", "left" => { "k" => "other" }, "right" => enc(s[2]), "line" => 0 }
  when "if", "unless", "elsif"
    { "k" => "if", "test" => enc(s[1]), "body" => enc_stmts(s[2]), "els" => else_of(s[3]), "line" => call_line(s[1]) }
  when "if_mod", "unless_mod"
    { "k" => "if", "test" => enc(s[1]), "body" => [enc_stmt(s[2])], "els" => nil, "line" => call_line(s[1]) }
  when "while", "until", "while_mod", "until_mod", "for"
    body = s[0].end_with?("_mod") ? [enc_stmt(s[2])] : enc_stmts(s[2])
    { "k" => "for", "body" => body, "line" => 0 }
  when "case"
    { "k" => "switch", "cases" => enc_cases(s[2]), "line" => 0 }
  when "return", "return0"
    { "k" => "return", "argument" => enc(s[1]), "line" => call_line(s) }
  when "def"
    add_func(ident_name(s[1]), s[2], s[3]); { "k" => "funcref" }
  when "defs"                                          # def self.name
    add_func(ident_name(s[3]), s[4], s[5]); { "k" => "funcref" }
  when "class", "module"
    collect_defs(s); { "k" => "other" }
  when "begin"
    { "k" => "block", "body" => enc_stmts(body_of(s[1])) }
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
  cases << { "k" => "case", "body" => enc_stmts(cur[1]) } if cur.is_a?(Array) && cur[0].to_s == "else"
  cases
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
