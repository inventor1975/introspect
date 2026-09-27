require "sinatra/base"
require "tilt/erb"

class NewsletterApp < Sinatra::Base
  post "/newsletters/render" do
    layout_source = params[:layout].to_s
    template = Tilt["erb"].new { layout_source }
    template.render(self, issue: params[:issue_number].to_i)
  end
end
