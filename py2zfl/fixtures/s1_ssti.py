tpl = request.args['tpl']
render_template_string(tpl)   # EXPECT: REFUTED [ssti]
