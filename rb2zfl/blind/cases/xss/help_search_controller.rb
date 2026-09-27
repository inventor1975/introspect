class HelpSearchController < ApplicationController
  include ERB::Util

  TOPICS = ['Resetting your password', 'Billing cycles', 'Exporting data', 'Two-factor login'].freeze

  def results
    query = params[:q].to_s
    hits = TOPICS.grep(/#{Regexp.escape(query)}/i)
    list = hits.map { |title| "<li>#{h(title)}</li>" }.join
    render html: "<p>You searched for <mark>#{h(query)}</mark></p><ul>#{list}</ul>".html_safe
  end
end
