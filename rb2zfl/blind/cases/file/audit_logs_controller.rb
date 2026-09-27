class AuditLogsController < ApplicationController
  LOG_FILES = %w[audit.log audit.log.1 audit.log.2].freeze

  def show
    file = LOG_FILES[params[:n].to_i]
    return head(:not_found) if file.nil?

    send_file Rails.root.join("log", file), type: "text/plain"
  end
end
