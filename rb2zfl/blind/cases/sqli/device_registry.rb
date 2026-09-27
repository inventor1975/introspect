require "sinatra/base"

class DeviceRegistry < Sinatra::Base
  get "/devices" do
    firmware = params[:firmware]
    conn = ActiveRecord::Base.connection
    conn.exec_query("SELECT * FROM devices WHERE firmware = '#{firmware}'").to_a.to_json
  end
end
