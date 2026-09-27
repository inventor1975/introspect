require "sinatra"

PAGES = {
  "billing" => :help_billing,
  "account" => :help_account,
  "shipping" => :help_shipping
}.freeze

get "/help" do
  @query = params[:q]
  template = PAGES.fetch(params[:page], :help_index)
  erb template
end
