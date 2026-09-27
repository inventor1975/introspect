require "sinatra"
require "time"

FEEDBACK_LOG = "/var/log/myapp/feedback.log".freeze

post "/feedback" do
  message = params[:message].to_s.tr("\r\n", "  ")
  from = params[:email].to_s[0, 120]

  File.open(FEEDBACK_LOG, "a") do |f|
    f.puts("#{Time.now.utc.iso8601}\t#{from}\t#{message}")
  end

  redirect "/thanks"
end
