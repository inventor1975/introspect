class PagesController
  def show
    msg = params[:msg]
    render html: raw(msg)           # EXPECT: REFUTED [xss] (raw bypasses escaping)
  end
end
