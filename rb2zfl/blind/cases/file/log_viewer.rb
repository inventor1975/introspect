require "sinatra/base"

class LogViewer < Sinatra::Base
  LOG_DIR = "/var/log/myapp".freeze

  get "/logs" do
    content_type "text/plain"
    begin
      File.read("#{LOG_DIR}/#{params[:log]}")
    rescue Errno::ENOENT, Errno::EISDIR
      halt 404, "no such log"
    end
  end
end
