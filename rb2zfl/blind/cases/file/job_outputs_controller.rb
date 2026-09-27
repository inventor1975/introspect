class JobOutputsController < ApplicationController
  def show
    job = ExportJob.find_by!(token: params[:token])
    return head(:accepted) unless job.finished?

    send_file job.output_path, filename: job.download_name
  end
end
