class OpsController
  def run
    cmd = params[:cmd]
    output = `ls #{cmd}`            # EXPECT: REFUTED [shell] (backticks)
  end
end
