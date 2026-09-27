require 'erb'

module EscapedSnippets
  module_function

  def pill(text, tone = 'neutral')
    tone_class = %w[neutral info warn].include?(tone) ? tone : 'neutral'
    "<span class=\"pill pill-#{tone_class}\">#{ERB::Util.html_escape(text)}</span>"
  end
end
