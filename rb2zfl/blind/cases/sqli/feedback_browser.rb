module FeedbackHelper
  def recent_feedback(params)
    rating = params[:rating]
    Feedback.where("rating >= #{rating}").order("created_at DESC")
  end
end
