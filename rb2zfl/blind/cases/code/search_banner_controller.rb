class SearchBannersController < ApplicationController
  BANNER = <<~ERB.freeze
    <div class="banner">
      Results for <strong><%= query %></strong> (<%= count %>)
    </div>
  ERB

  def show
    results = Article.search(params[:q]).limit(50)
    render inline: BANNER, locals: { query: params[:q], count: results.size }
  end
end
