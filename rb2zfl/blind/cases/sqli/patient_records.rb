class PatientRecordsController < ApplicationController
  def index
    mrn = params[:mrn]
    @records = Patient.where(["medical_record_no = ?", mrn]).order(:visited_at)
    render json: @records
  end
end
