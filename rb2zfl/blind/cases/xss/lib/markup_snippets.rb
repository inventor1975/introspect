module MarkupSnippets
  module_function

  def status_chip(text, tone = 'neutral')
    "<span class=\"chip chip-#{tone}\">#{text}</span>"
  end

  def section(title, inner)
    "<section><h2>#{title}</h2>#{inner}</section>"
  end
end
