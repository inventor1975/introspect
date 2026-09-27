class TicketsController < ApplicationController
  def search
    priority = params[:priority]
    tickets = Ticket.joins(
      "INNER JOIN agents ON agents.id = tickets.agent_id AND agents.level = #{priority}"
    )
    render json: tickets
  end
end
