class NotificationPrefsController < ApplicationController
  def index
    channel = params[:channel]
    @prefs = Preference.joins(:user)
                       .where("preferences.channel = '#{channel}'")
    render json: @prefs
  end
end
