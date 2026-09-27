require "sinatra/base"

class MetricsApp < Sinatra::Base
  def db
    @db ||= Sequel.connect(ENV["METRICS_DB"])
  end

  get "/metrics/:name" do
    metric = params[:name]
    result = db.fetch("SELECT * FROM metrics WHERE name = '#{metric}'").all
    result.to_json
  end
end
