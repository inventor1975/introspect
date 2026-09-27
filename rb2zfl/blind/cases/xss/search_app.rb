require 'sinatra'

CATALOG = ['Blue Kettle', 'Cast Iron Pan', 'Chef Knife', 'Pepper Mill'].freeze

get '/search' do
  term = params['q'].to_s
  results = CATALOG.select { |item| item.downcase.include?(term.downcase) }
  list = results.map { |item| "<li>#{item}</li>" }.join
  "<h2>Results for #{term}</h2><ul>#{list}</ul>"
end
