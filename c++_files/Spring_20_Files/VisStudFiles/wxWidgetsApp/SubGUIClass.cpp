#include "SubGUIClass.h"

SubGUIClass::SubGUIClass( wxWindow* parent )
:
GUIClass( parent )
{

}

void SubGUIClass::OnExit( wxCommandEvent& event )
{
	int answer = wxMessageBox("Do you want to exit?", "Exit Confirmation", wxYES | wxNO, this);
	if (answer == wxYES) Close();
}

void SubGUIClass::OnAboutSelect( wxCommandEvent& event )
{
	wxMessageBox("About: Hello World", "About", wxOK, this);
}
