class ListController < ApplicationController
  ALLOWED = %w[name price].freeze
  def index
    sort = ALLOWED.include?(params[:s]) ? params[:s] : "name"
    Item.order("#{sort} ASC")
    File.read("columns/#{sort}.txt")
    x = params[:a] || "id"
    Item.order("#{x} DESC")
  end
end
