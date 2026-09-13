class ToolController
  def run_cmd(c)
    system(c)                       # param -> shell (summary)
  end
  def index
    cmd = params[:cmd]
    run_cmd(cmd)                    # EXPECT: REFUTED (cross-method summary)
    run_cmd("safe")                 # EXPECT: clean
  end
end
