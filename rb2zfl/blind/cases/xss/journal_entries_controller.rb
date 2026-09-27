class JournalEntriesController < ApplicationController
  def create
    entry = JournalEntry.create!(title: params[:title], body: params[:body], user_id: session[:user_id])
    redirect_to journal_entry_path(entry)
  end

  def show
    entry = JournalEntry.find(params[:id])
    render html: "<article><h1>#{ERB::Util.h(entry.title)}</h1>#{entry.body}</article>".html_safe
  end
end
