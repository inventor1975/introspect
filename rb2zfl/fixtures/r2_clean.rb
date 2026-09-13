class PagesController
  def show
    q = params[:q]                  # unused in any sink
    system("uptime")                # constant: EXPECT nothing
    User.where(active: true)        # hash arg, not a tainted string: EXPECT nothing
  end
end
