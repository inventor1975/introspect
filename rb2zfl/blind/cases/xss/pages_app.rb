require 'sinatra'

PAGES = { 'about' => '<p>About us</p>', 'team' => '<p>Our team</p>' }.freeze

get '/pages/:slug' do
  page = PAGES[params[:slug]]
  halt 404, "<h1>No page named #{params[:slug]}</h1>" unless page
  "<main>#{page}</main>"
end
