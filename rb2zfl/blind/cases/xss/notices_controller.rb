class NoticesController < ApplicationController
  def flash_banner
    render html: notice_markup(params[:message], params[:level])
  end

  private

  def notice_markup(text, level)
    css = %w[info warning error].include?(level) ? level : 'info'
    format('<div class="notice notice-%s">%s</div>', css, text).html_safe
  end
end
