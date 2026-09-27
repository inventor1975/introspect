class Transaction < ApplicationRecord
  def self.for_account(params)
    acct = params[:account]
    where("account_no = '#{acct}'").order(Arel.sql(params[:sort]))
  end
end
