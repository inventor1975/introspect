require 'sinatra'
require 'rack/utils'

GLOSSARY = {
  'latency' => 'Time taken for a request to travel to the server and back.',
  'throughput' => 'Requests handled per unit of time.'
}.freeze

get '/lookup' do
  word = params[:word].to_s
  definition = GLOSSARY.fetch(word.downcase, 'No definition found.')
  "<dl><dt>#{Rack::Utils.escape_html(word)}</dt><dd>#{definition}</dd></dl>"
end
