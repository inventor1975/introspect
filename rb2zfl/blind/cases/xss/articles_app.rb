require 'sinatra'
require 'erb'

ARTICLES = { 'intro' => '<p>Introduction</p>', 'faq' => '<p>Frequently asked questions</p>' }.freeze

get '/articles/:name' do
  article = ARTICLES[params[:name]]
  halt 404, "<h1>No article called #{ERB::Util.html_escape(params[:name])}</h1>" if article.nil?
  "<article>#{article}</article>"
end
