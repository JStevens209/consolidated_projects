///////////////////////////////////////////////////////////////////////////
// C++ code generated with wxFormBuilder (version Jun 30 2011)
// http://www.wxformbuilder.org/
//
// PLEASE DO "NOT" EDIT THIS FILE!
///////////////////////////////////////////////////////////////////////////

#include "GUIClass.h"

///////////////////////////////////////////////////////////////////////////

GUIClass::GUIClass( wxWindow* parent, wxWindowID id, const wxString& title, const wxPoint& pos, const wxSize& size, long style ) : wxFrame( parent, id, title, pos, size, style )
{
	this->SetSizeHints( wxDefaultSize, wxDefaultSize );
	
	menuBar = new wxMenuBar( 0 );
	fileMenu = new wxMenu();
	wxMenuItem* exitItem;
	exitItem = new wxMenuItem( fileMenu, wxID_ANY, wxString( wxT("Exit") ) + wxT('\t') + wxT("ALT-F4"), wxEmptyString, wxITEM_NORMAL );
	fileMenu->Append( exitItem );
	
	menuBar->Append( fileMenu, wxT("File") ); 
	
	helpMenu = new wxMenu();
	wxMenuItem* aboutItem;
	aboutItem = new wxMenuItem( helpMenu, wxID_ANY, wxString( wxT("About") ) + wxT('\t') + wxT("ALT-A"), wxEmptyString, wxITEM_NORMAL );
	helpMenu->Append( aboutItem );
	
	menuBar->Append( helpMenu, wxT("Help") ); 
	
	this->SetMenuBar( menuBar );
	
	wxBoxSizer* bSizer1;
	bSizer1 = new wxBoxSizer( wxVERTICAL );
	
	m_panel1 = new wxPanel( this, wxID_ANY, wxDefaultPosition, wxDefaultSize, wxTAB_TRAVERSAL );
	wxBoxSizer* panelSizer;
	panelSizer = new wxBoxSizer( wxVERTICAL );
	
	wxBoxSizer* bSizer3;
	bSizer3 = new wxBoxSizer( wxHORIZONTAL );
	
	m_button1 = new wxButton( m_panel1, wxID_ANY, wxT("MyButton"), wxDefaultPosition, wxDefaultSize, 0 );
	bSizer3->Add( m_button1, 0, wxALL, 5 );
	
	m_button2 = new wxButton( m_panel1, wxID_ANY, wxT("MyButton"), wxDefaultPosition, wxDefaultSize, 0 );
	bSizer3->Add( m_button2, 0, wxALL, 5 );
	
	m_button3 = new wxButton( m_panel1, wxID_ANY, wxT("MyButton"), wxDefaultPosition, wxDefaultSize, 0 );
	bSizer3->Add( m_button3, 0, wxALL, 5 );
	
	panelSizer->Add( bSizer3, 1, wxEXPAND, 5 );
	
	wxBoxSizer* panelSizer1;
	panelSizer1 = new wxBoxSizer( wxVERTICAL );
	
	wxBoxSizer* bSizer31;
	bSizer31 = new wxBoxSizer( wxHORIZONTAL );
	
	m_button11 = new wxButton( m_panel1, wxID_ANY, wxT("MyButton"), wxDefaultPosition, wxDefaultSize, 0 );
	bSizer31->Add( m_button11, 0, wxALL, 5 );
	
	m_button21 = new wxButton( m_panel1, wxID_ANY, wxT("MyButton"), wxDefaultPosition, wxDefaultSize, 0 );
	bSizer31->Add( m_button21, 0, wxALL, 5 );
	
	m_button31 = new wxButton( m_panel1, wxID_ANY, wxT("MyButton"), wxDefaultPosition, wxDefaultSize, 0 );
	bSizer31->Add( m_button31, 0, wxALL, 5 );
	
	panelSizer1->Add( bSizer31, 1, wxEXPAND, 5 );
	
	panelSizer->Add( panelSizer1, 1, wxEXPAND, 5 );
	
	m_panel1->SetSizer( panelSizer );
	m_panel1->Layout();
	panelSizer->Fit( m_panel1 );
	bSizer1->Add( m_panel1, 1, wxEXPAND | wxALL, 5 );
	
	this->SetSizer( bSizer1 );
	this->Layout();
	m_statusBar2 = this->CreateStatusBar( 1, wxST_SIZEGRIP, wxID_ANY );
	
	this->Centre( wxBOTH );
	
	// Connect Events
	this->Connect( exitItem->GetId(), wxEVT_COMMAND_MENU_SELECTED, wxCommandEventHandler( GUIClass::OnExit ) );
	this->Connect( aboutItem->GetId(), wxEVT_COMMAND_MENU_SELECTED, wxCommandEventHandler( GUIClass::OnAboutSelect ) );
}

GUIClass::~GUIClass()
{
	// Disconnect Events
	this->Disconnect( wxID_ANY, wxEVT_COMMAND_MENU_SELECTED, wxCommandEventHandler( GUIClass::OnExit ) );
	this->Disconnect( wxID_ANY, wxEVT_COMMAND_MENU_SELECTED, wxCommandEventHandler( GUIClass::OnAboutSelect ) );
	
}
