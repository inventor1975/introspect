class AccountProfileController < ApplicationController
  def show
    @account = Account.where("email = ?", params[:email]).first
    render json: @account
  end
end
