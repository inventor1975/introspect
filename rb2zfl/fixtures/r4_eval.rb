class CalcController
  def run
    expr = params[:expr]
    eval(expr)                      # EXPECT: REFUTED [code]
  end
end
