// goast — thin Go AST -> JSON dumper for go2zfl (the introspect's Go module).
// Uses Go's OWN go/parser+go/ast (the gold-standard parser). Emits a compact typed
// tree of just the nodes the taint analyzer needs. Usage: goast <file.go>  (JSON to stdout).
package main

import (
	"strings"
	"encoding/json"
	"go/ast"
	"go/parser"
	"go/token"
	"os"
)

var fset *token.FileSet

func line(p token.Pos) int {
	if p == token.NoPos {
		return 0
	}
	return fset.Position(p).Line
}

// enc encodes an expression node into a compact map.
func enc(n ast.Expr) map[string]interface{} {
	switch e := n.(type) {
	case *ast.Ident:
		return map[string]interface{}{"k": "ident", "name": e.Name}
	case *ast.BasicLit:
		return map[string]interface{}{"k": "lit", "kind": e.Kind.String(), "value": e.Value}
	case *ast.BinaryExpr:
		return map[string]interface{}{"k": "bin", "op": e.Op.String(), "x": enc(e.X), "y": enc(e.Y)}
	case *ast.CallExpr:
		args := []interface{}{}
		for _, a := range e.Args {
			args = append(args, enc(a))
		}
		return map[string]interface{}{"k": "call", "fun": enc(e.Fun), "args": args, "line": line(e.Lparen)}
	case *ast.SelectorExpr:
		return map[string]interface{}{"k": "sel", "x": enc(e.X), "sel": e.Sel.Name}
	case *ast.IndexExpr:
		return map[string]interface{}{"k": "index", "x": enc(e.X), "index": enc(e.Index)}
	case *ast.StarExpr:
		return map[string]interface{}{"k": "star", "x": enc(e.X)}
	case *ast.ParenExpr:
		return enc(e.X)
	case *ast.UnaryExpr:
		return map[string]interface{}{"k": "unary", "op": e.Op.String(), "x": enc(e.X)}
	case *ast.CompositeLit:
		elts := []interface{}{}
		for _, el := range e.Elts {
			elts = append(elts, enc(el))
		}
		return map[string]interface{}{"k": "composite", "typ": typeName(e.Type), "elts": elts}
	case *ast.KeyValueExpr:
		return map[string]interface{}{"k": "kv", "key": enc(e.Key), "value": enc(e.Value)}
	case *ast.TypeAssertExpr:
		return map[string]interface{}{"k": "typeassert", "x": enc(e.X)}
	case *ast.SliceExpr:
		return map[string]interface{}{"k": "slice", "x": enc(e.X)}
	case *ast.FuncLit:
		// a closure: HandleFunc(.., func(w, r) {..}), go func() {..}(), Transaction(func(tx) ..)
		return map[string]interface{}{"k": "funclit", "params": encFields(e.Type.Params), "body": encBlock(e.Body),
			"line": line(e.Pos())}
	case nil:
		return map[string]interface{}{"k": "nil"}
	default:
		return map[string]interface{}{"k": "other"}
	}
}

func typeName(e ast.Expr) string {
	switch t := e.(type) {
	case *ast.Ident:
		return t.Name
	case *ast.SelectorExpr:
		return typeName(t.X) + "." + t.Sel.Name
	case *ast.StarExpr:
		return typeName(t.X)
	case *ast.ArrayType:
		return "[]" + typeName(t.Elt)
	case *ast.MapType:
		return "map"
	default:
		return ""
	}
}

func encStmt(s ast.Stmt) map[string]interface{} {
	switch st := s.(type) {
	case *ast.AssignStmt:
		lhs, rhs := []interface{}{}, []interface{}{}
		for _, x := range st.Lhs {
			lhs = append(lhs, enc(x))
		}
		for _, x := range st.Rhs {
			rhs = append(rhs, enc(x))
		}
		return map[string]interface{}{"k": "assign", "tok": st.Tok.String(), "lhs": lhs, "rhs": rhs, "line": line(st.TokPos)}
	case *ast.ExprStmt:
		return map[string]interface{}{"k": "exprstmt", "x": enc(st.X), "line": line(st.Pos())}
	case *ast.IfStmt:
		m := map[string]interface{}{"k": "if", "cond": enc(st.Cond), "body": encBlock(st.Body), "line": line(st.If)}
		if st.Init != nil {
			m["init"] = encStmt(st.Init)
		}
		if st.Else != nil {
			m["els"] = encStmt(st.Else) // BlockStmt or IfStmt
		}
		return m
	case *ast.BlockStmt:
		return map[string]interface{}{"k": "block", "body": encBlock(st)}
	case *ast.ForStmt:
		return map[string]interface{}{"k": "for", "body": encBlock(st.Body), "line": line(st.For)}
	case *ast.RangeStmt:
		m := map[string]interface{}{"k": "range", "x": enc(st.X), "body": encBlock(st.Body), "line": line(st.For),
			"tok": st.Tok.String()}
		if st.Key != nil {
			m["key"] = enc(st.Key)
		}
		if st.Value != nil {
			m["value"] = enc(st.Value)
		}
		return m
	case *ast.ReturnStmt:
		res := []interface{}{}
		for _, r := range st.Results {
			res = append(res, enc(r))
		}
		return map[string]interface{}{"k": "return", "results": res, "line": line(st.Return)}
	case *ast.DeclStmt:
		// var x = expr  /  var x T = expr
		vars := []interface{}{}
		if gd, ok := st.Decl.(*ast.GenDecl); ok {
			for _, spec := range gd.Specs {
				if vs, ok := spec.(*ast.ValueSpec); ok {
					names := []interface{}{}
					for _, nm := range vs.Names {
						names = append(names, nm.Name)
					}
					vals := []interface{}{}
					for _, v := range vs.Values {
						vals = append(vals, enc(v))
					}
					vars = append(vars, map[string]interface{}{"names": names, "values": vals, "typ": typeName(vs.Type)})
				}
			}
		}
		return map[string]interface{}{"k": "var", "vars": vars, "line": line(st.Pos())}
	case *ast.SwitchStmt:
		m := map[string]interface{}{"k": "switch", "body": encBlock(st.Body), "line": line(st.Switch)}
		if st.Tag != nil {
			m["tag"] = enc(st.Tag)
		}
		if st.Init != nil {
			m["init"] = encStmt(st.Init)
		}
		return m
	case *ast.TypeSwitchStmt:
		return map[string]interface{}{"k": "switch", "body": encBlock(st.Body), "line": line(st.Switch)}
	case *ast.CaseClause:
		body := []interface{}{}
		for _, s2 := range st.Body {
			body = append(body, encStmt(s2))
		}
		list := []interface{}{}
		for _, e := range st.List {
			list = append(list, enc(e))
		}
		return map[string]interface{}{"k": "case", "body": body, "list": list}
	case *ast.SelectStmt:
		return map[string]interface{}{"k": "block", "body": encBlock(st.Body)}
	case *ast.CommClause:
		body := []interface{}{}
		for _, s2 := range st.Body {
			body = append(body, encStmt(s2))
		}
		return map[string]interface{}{"k": "case", "body": body}
	case *ast.LabeledStmt:
		return encStmt(st.Stmt)
	case *ast.DeferStmt:
		return map[string]interface{}{"k": "exprstmt", "x": enc(st.Call), "line": line(st.Defer)}
	case *ast.BranchStmt:
		return map[string]interface{}{"k": "branch", "tok": st.Tok.String(), "line": line(st.Pos())}
	case *ast.SendStmt:
		return map[string]interface{}{"k": "assign", "tok": "<-", "lhs": []interface{}{enc(st.Chan)},
			"rhs": []interface{}{enc(st.Value)}, "line": line(st.Arrow)}
	case *ast.GoStmt:
		return map[string]interface{}{"k": "exprstmt", "x": enc(st.Call), "line": line(st.Go)}
	default:
		return map[string]interface{}{"k": "other"}
	}
}

func encBlock(b *ast.BlockStmt) []interface{} {
	out := []interface{}{}
	if b == nil {
		return out
	}
	for _, s := range b.List {
		out = append(out, encStmt(s))
	}
	return out
}

func encFields(fl *ast.FieldList) []interface{} {
	out := []interface{}{}
	if fl == nil {
		return out
	}
	for _, f := range fl.List {
		tn := typeName(f.Type)
		tag := ""
		if f.Tag != nil {
			tag = strings.Trim(f.Tag.Value, "`")
		}
		if len(f.Names) == 0 {
			out = append(out, map[string]interface{}{"name": "", "typ": tn, "tag": tag})
		}
		for _, nm := range f.Names {
			out = append(out, map[string]interface{}{"name": nm.Name, "typ": tn, "tag": tag})
		}
	}
	return out
}

func main() {
	if len(os.Args) < 2 {
		os.Exit(2)
	}
	fset = token.NewFileSet()
	f, err := parser.ParseFile(fset, os.Args[1], nil, 0)
	if err != nil {
		// emit an error marker but still exit 0 so the caller can skip gracefully
		json.NewEncoder(os.Stdout).Encode(map[string]interface{}{"k": "file", "error": err.Error(), "funcs": []interface{}{}})
		return
	}
	globals := []interface{}{}
	types := []interface{}{}
	for _, decl := range f.Decls {
		gd, ok := decl.(*ast.GenDecl)
		if !ok {
			continue
		}
		for _, spec := range gd.Specs {
			ts, ok := spec.(*ast.TypeSpec)
			if !ok {
				continue
			}
			if st, ok := ts.Type.(*ast.StructType); ok {
				types = append(types, map[string]interface{}{"name": ts.Name.Name, "fields": encFields(st.Fields)})
			}
		}
	}
	for _, decl := range f.Decls {
		gd, ok := decl.(*ast.GenDecl)
		if !ok {
			continue
		}
		for _, spec := range gd.Specs {
			vs, ok := spec.(*ast.ValueSpec)
			if !ok {
				continue
			}
			for i, nm := range vs.Names {
				val := map[string]interface{}{"k": "nil"}
				if i < len(vs.Values) {
					val = enc(vs.Values[i])
				}
				globals = append(globals, map[string]interface{}{"name": nm.Name, "value": val,
					"const": gd.Tok == token.CONST, "typ": typeName(vs.Type)})
			}
		}
	}
	funcs := []interface{}{}
	for _, decl := range f.Decls {
		fd, ok := decl.(*ast.FuncDecl)
		if !ok {
			continue
		}
		m := map[string]interface{}{
			"k":      "func",
			"name":   fd.Name.Name,
			"recv":   encFields(fd.Recv),
			"params": encFields(paramsOf(fd)),
			"results": encFields(fd.Type.Results),
			"body":   encBlock(fd.Body),
			"line":   line(fd.Pos()),
		}
		funcs = append(funcs, m)
	}
	imports := []interface{}{}
	for _, imp := range f.Imports {
		path := strings.Trim(imp.Path.Value, "\"")
		segs := strings.Split(path, "/")
		name := segs[len(segs)-1]
		if len(segs) > 1 && len(name) > 1 && name[0] == 'v' && strings.Trim(name[1:], "0123456789") == "" {
			name = segs[len(segs)-2] // .../chi/v5 -> chi
		}
		if i := strings.Index(name, ".v"); i > 0 {
			name = name[:i] // yaml.v3 -> yaml
		}
		name = strings.TrimPrefix(name, "go-")
		if imp.Name != nil {
			name = imp.Name.Name
		}
		imports = append(imports, map[string]interface{}{"name": name, "path": path})
	}
	json.NewEncoder(os.Stdout).Encode(map[string]interface{}{"k": "file", "pkg": f.Name.Name, "funcs": funcs,
		"globals": globals, "imports": imports, "types": types})
}

func paramsOf(fd *ast.FuncDecl) *ast.FieldList {
	if fd.Type == nil {
		return nil
	}
	return fd.Type.Params
}
