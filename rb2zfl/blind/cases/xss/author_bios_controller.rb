class AuthorBiosController < ApplicationController
  def preview
    bio = helpers.sanitize(params[:bio], tags: %w[p br strong em a], attributes: %w[href title])
    render html: "<section class=\"bio\">#{bio}</section>".html_safe
  end
end
