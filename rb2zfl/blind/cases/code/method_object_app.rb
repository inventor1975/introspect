require "sinatra"

class StatsCalculator
  def mean(*xs)
    xs.map(&:to_f).sum / xs.size
  end

  def max(*xs)
    xs.map(&:to_f).max
  end
end

get "/stats/:fn" do
  calc = StatsCalculator.new
  fn = calc.method(params[:fn])
  values = params[:values].to_s.split(",")
  fn.call(*values).to_s
end
