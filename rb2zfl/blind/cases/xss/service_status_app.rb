require 'sinatra'

get '/status' do
  notice = ENV.fetch('MAINTENANCE_NOTICE_HTML', '')
  service = Rack::Utils.escape_html(params[:service].to_s)
  "<div class=\"notice\">#{notice}</div><p>Status for #{service}: operational</p>"
end
