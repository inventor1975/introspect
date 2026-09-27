class LegacyAccountsController < ApplicationController
  def show
    account = Account.find_by_sql(
      "SELECT * FROM accounts WHERE legacy_ref = " + params[:ref]
    ).first
    render json: account
  end
end
