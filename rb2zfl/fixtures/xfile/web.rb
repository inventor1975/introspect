class WebController
  def show
    id = params[:id]
    Dao.new.q(id)                   # EXPECT: REFUTED cross-file (q param -> sql)
  end
end
