class C
  def show
    msg = params[:msg]
    x = raw(ERB::Util.html_escape(msg))   # clean: escaped for xss
    y = raw(msg)                           # EXPECT: REFUTED [xss]
  end
end
