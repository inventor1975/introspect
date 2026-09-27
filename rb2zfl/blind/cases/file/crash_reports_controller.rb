class CrashReportsController < ApplicationController
  REPORTS = "/var/app/crash_reports".freeze

  before_action :set_report_path

  def show
    send_file @report_path, type: "text/plain", disposition: "inline"
  end

  def destroy
    File.delete(@report_path)
    head :no_content
  end

  private

  def set_report_path
    @report_path = File.join(REPORTS, params[:id].to_s + ".txt")
  end
end
