#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QFileDialog>
#include <QFile>
#include <QTextStream>
#include <vector>


MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    const QString currLetter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

    for(int i = 0; i < 26; i++){
        cipherToPlaintextKeys[i][0] = currLetter[i];
        ciphertextFreq[i][0] = currLetter[i];

        updatePlaintextFreq();
        get_cipherText_Freq();
        updateFrequencyTables();
    }
}

MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::on_browse_clicked()
{
    QString fileName = QFileDialog::getOpenFileName(this,tr("Open Text File"), "/User", tr("Text Files (*.txt )"));
    ui->filePath->insert(fileName);
}

void MainWindow::on_browseCipher_clicked()
{
    QString fileName = QFileDialog::getOpenFileName(this,tr("Open Text File"), "/User", tr("Text Files (*.txt )"));
    QFile file(fileName);
        if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
            return;

        QTextStream in( &file );
        while ( !in.atEnd() ) {
            QString line = in.readLine();
            line = line.toUpper();
            ui->cipherTextEdit->insertPlainText(line);
        }

        get_cipherText_Freq();
        updateFrequencyTables();
}


void MainWindow::on_guess_clicked()
{    
    QString cipherText = ui->cipherTextEdit->toPlainText();


    for( int i = 0; i < cipherText.length(); i++ ){
        for(int j = 0; j < 26; j++){
            if( cipherText[i] == cipherToPlaintextKeys[j][0].at(0) ){
                cipherText[i] = cipherToPlaintextKeys[j][1].at(0);
                break;
            }
        }
    }

    QList<QLineEdit* > lineEditArray = {
        ui->A_EditBox,
        ui->B_EditBox,
        ui->C_EditBox,
        ui->D_EditBox,
        ui->E_EditBox,
        ui->F_EditBox,
        ui->G_EditBox,
        ui->H_EditBox,
        ui->I_EditBox,
        ui->J_EditBox,
        ui->K_EditBox,
        ui->L_EditBox,
        ui->M_EditBox,
        ui->N_EditBox,
        ui->O_EditBox,
        ui->P_EditBox,
        ui->Q_EditBox,
        ui->R_EditBox,
        ui->S_EditBox,
        ui->T_EditBox,
        ui->U_EditBox,
        ui->V_EditBox,
        ui->W_EditBox,
        ui->X_EditBox,
        ui->Y_EditBox,
        ui->Z_EditBox
    };
    const QString currLetter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

    for( int i = 0; i < 26; i++){
        for( int j = 0; j < 26; j++){
            if( currLetter[i] == cipherToPlaintextKeys[j][0].at(0) ){
                lineEditArray[i]->setText( cipherToPlaintextKeys[j][1].toLower() );
            }
        }
    }

    ui->plainTextEdit->setPlainText( cipherText.toLower() );

}


void MainWindow::on_EditBox_textChanged( const QString &arg1 )
{
    QString arg = arg1.toUpper();
    if( arg1.length() > 1 ){
        for( int i = 0; i < 26; i++ ){
            if( arg1[0] == cipherToPlaintextKeys[i][0] ){
                cipherToPlaintextKeys[i][1] = arg1[1];
                break;
            }
        }

        ui->guess->clicked();
    }
}

void MainWindow::on_calibrate_clicked()
{
    QString fileText;
    QString filePath = ui->filePath->text();
    QFile file( filePath );

    if (file.open(QIODevice::ReadOnly | QIODevice::Text)) {


        QTextStream in( &file );
        while ( !in.atEnd() ) {
            QString line = in.readLine();
            line = line.toLower();
            fileText.append(line);
        }

        updatePlaintextFreq( fileText, false );
    }
    else{
        updatePlaintextFreq();
    }

    get_cipherText_Freq();

    updateFrequencyTables();
}



void MainWindow::get_cipherText_Freq(){
    QString text = ui->cipherTextEdit->toPlainText();
    const QString currLetter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    double letterCount;
    double letterFrequencies[26] = {};

    if( text.length() > 0 ) {

        text = text.remove(' ');
        double length = text.length();

        for(int i = 0; i < 26; i++ ){
            letterCount = 0;

            for(int j = 0; j < length; j++){
                if( text.at(j) == currLetter[i] ){
                    letterCount++;
                }
            }

            letterFrequencies[i] = ((letterCount / length ) * 100);
        }

        for(int i = 0; i < 26; i++){
            ciphertextFreq[i][1] = (QString::number(letterFrequencies[i]));
            ciphertextFreq[i][0] = currLetter[i];
        }

   }
}

// I created this because just look at the first if statement of
// updatePlaintextFreq()
// ... That would've been awful lol
void MainWindow::ptVectSet(QString l, QString n) {
    // make a vector that holds the current loop cycles
    // letter and the number of times it appeared
    std::vector<QString> letterSet;
    letterSet.push_back(l);
    letterSet.push_back(n);
    // push this into the plaintext frequency vector
    plaintextFreq.push_back(letterSet);
}

// string str is the plaintext for comparing frequencies
// MAKE SURE YOU PASS A bool AS THE LAST PARAMETER!!!
// bool isDefault is whether or not default english is selected ==> if true, then default english
void MainWindow::updatePlaintextFreq(const QString str, bool isDefault) {
    plaintextFreq.clear();

    if (isDefault) {
        // I just multiplied their percentages by 1000
        // They are in order of the alphabet. I did this because every other time I
        // filled a vector, I also did it in alphabetical order. Maybe this will make the
        // graph/table a little easier
        ptVectSet("A","8.2");
        ptVectSet("B", "1.5");
        ptVectSet("C", "2.8");
        ptVectSet("D", "4.3");
        ptVectSet("E", "13.0");
        ptVectSet("F", "2.2");
        ptVectSet("G", "2.0");
        ptVectSet("H", "6.1");
        ptVectSet("I", "7.0");
        ptVectSet("J", ".15");
        ptVectSet("K", ".77");
        ptVectSet("L", "4.0");
        ptVectSet("M", "2.4");
        ptVectSet("N", "6.7");
        ptVectSet("O","7.5");
        ptVectSet("P", "1.9");
        ptVectSet("Q", "0.095");
        ptVectSet("R", "6.0");
        ptVectSet("S", "6.3");
        ptVectSet("T", "9.1");
        ptVectSet("U", "2.8");
        ptVectSet("V", "0.98");
        ptVectSet("W", "2.4");
        ptVectSet("X", "0.15");
        ptVectSet("Y", "2.0");
        ptVectSet("Z", "0.074");
    }
    else {
        QString plainText = str.toUpper();
        // for each letter of the alphabet
        // counts number of a specific character
        // letter is the letter that is associated to this loop cycle
        const QString currLetter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

        for (int i = 0; i < 26; i++) {
            // for each char in the string passed to the function by parameter
            double charCount = 0;
            for (int j = 0; j < str.length(); j++) {
                // if a char in the string is the letter that is currently being counted,
                // increment the counter
                if (currLetter[i] == plainText[j]) {
                    charCount++;
                }
            }

            // make a vector that holds the current loop cycles letter and the number of times it appeared
            ptVectSet(QString(1, currLetter[i]), QString::number((charCount / str.length() * 100)));
        }
    }
}

//Bubble sort, push to table
void MainWindow::updateFrequencyTables(){

    ui->expectedFreq->setSortingEnabled( false );
    ui->cipherFreq->setSortingEnabled( false );

    bool notSorted = true;
    bool swapPerformed = false;


    while( notSorted ){

        swapPerformed = false;

        for(int i = 0; i < 25; i++){

            if( ciphertextFreq[i][1].toDouble() < ciphertextFreq[i+1][1].toDouble() ){
                std::swap( ciphertextFreq[i], ciphertextFreq[i+1]);
                swapPerformed = true;
            }

            if( plaintextFreq[i][1].toDouble() < plaintextFreq[i+1][1].toDouble() ){
                std::swap( plaintextFreq[i], plaintextFreq[i+1] );
                swapPerformed = true;
            }
        }

        if( swapPerformed == false ){
            notSorted = false;
        }
    }

    for( int i = 0; i < 26; i++ ){
        for( int j = 0; j < 2; j++ ){
            auto cipherItem = new QTableWidgetItem( ciphertextFreq[i][j] );
            auto plaintextItem = new QTableWidgetItem( plaintextFreq[i][j] );

            ui->cipherFreq->setItem( i, j, cipherItem );
            ui->expectedFreq->setItem( i, j, plaintextItem );
        }
    }

    //Calibrates cipher-plaintext key pairings
    for( int i = 0; i < 26; i++){
       auto cipherItem = ui->cipherFreq->item(i, 0)->text();
       auto plainItem = ui->expectedFreq->item(i, 0)->text();

       cipherToPlaintextKeys[i][0] = cipherItem;
       cipherToPlaintextKeys[i][1] = plainItem;

       QString letterPair = (cipherToPlaintextKeys[i][0] + cipherToPlaintextKeys[i][1]);
    }
}




//Pain and suffering, I needed a way to differentiate between who was calling on_edit_textChanged. Forgive me, me.
void MainWindow::on_A_EditBox_textChanged(const QString &arg1)
{
    QString letter = "A";
    on_EditBox_textChanged( (letter + arg1 ) );
}

void MainWindow::on_B_EditBox_textChanged(const QString &arg1)
{
    QString letter = "B";
    on_EditBox_textChanged( (letter + arg1 ) );
}

void MainWindow::on_C_EditBox_textChanged(const QString &arg1)
{
    QString letter = "C";
    on_EditBox_textChanged( (letter + arg1 ) );
}

void MainWindow::on_D_EditBox_textChanged(const QString &arg1)
{
    QString letter = "D";
    on_EditBox_textChanged( (letter + arg1 ) );
}

void MainWindow::on_E_EditBox_textChanged(const QString &arg1)
{
    QString letter = "E";
    on_EditBox_textChanged( (letter + arg1 ) );
}

void MainWindow::on_F_EditBox_textChanged(const QString &arg1)
{
    QString letter = "F";
    on_EditBox_textChanged( (letter + arg1 ) );
}

void MainWindow::on_G_EditBox_textChanged(const QString &arg1)
{
    QString letter = "G";
    on_EditBox_textChanged( (letter + arg1 ) );
}

void MainWindow::on_H_EditBox_textChanged(const QString &arg1)
{
    QString letter = "H";
    on_EditBox_textChanged( (letter + arg1 ) );
}

void MainWindow::on_I_EditBox_textChanged(const QString &arg1)
{
    QString letter = "I";
    on_EditBox_textChanged( (letter + arg1 ) );
}

void MainWindow::on_J_EditBox_textChanged(const QString &arg1)
{
    QString letter = "J";
    on_EditBox_textChanged( (letter + arg1 ) );
}

void MainWindow::on_K_EditBox_textChanged(const QString &arg1)
{
    QString letter = "K";
    on_EditBox_textChanged( (letter + arg1 ) );
}

void MainWindow::on_L_EditBox_textChanged(const QString &arg1)
{
    QString letter = "L";
    on_EditBox_textChanged( (letter + arg1 ) );
}

void MainWindow::on_M_EditBox_textChanged(const QString &arg1)
{
    QString letter = "M";
    on_EditBox_textChanged( (letter + arg1 ) );
}

void MainWindow::on_N_EditBox_textChanged(const QString &arg1)
{
    QString letter = "N";
    on_EditBox_textChanged( (letter + arg1 ) );
}

void MainWindow::on_O_EditBox_textChanged(const QString &arg1)
{
    QString letter = "O";
    on_EditBox_textChanged( (letter + arg1 ) );
}

void MainWindow::on_P_EditBox_textChanged(const QString &arg1)
{
    QString letter = "P";
    on_EditBox_textChanged( (letter + arg1 ) );
}

void MainWindow::on_Q_EditBox_textChanged(const QString &arg1)
{
    QString letter = "Q";
    on_EditBox_textChanged( (letter + arg1 ) );
}

void MainWindow::on_R_EditBox_textChanged(const QString &arg1)
{
    QString letter = "R";
    on_EditBox_textChanged( (letter + arg1 ) );
}

void MainWindow::on_S_EditBox_textChanged(const QString &arg1)
{
    QString letter = "S";
    on_EditBox_textChanged( (letter + arg1 ) );
}

void MainWindow::on_T_EditBox_textChanged(const QString &arg1)
{
    QString letter = "T";
    on_EditBox_textChanged( (letter + arg1 ) );
}

void MainWindow::on_U_EditBox_textChanged(const QString &arg1)
{
    QString letter = "U";
    on_EditBox_textChanged( (letter + arg1 ) );
}

void MainWindow::on_V_EditBox_textChanged(const QString &arg1)
{
    QString letter = "V";
    on_EditBox_textChanged( (letter + arg1 ) );
}

void MainWindow::on_W_EditBox_textChanged(const QString &arg1)
{
    QString letter = "W";
    on_EditBox_textChanged( (letter + arg1 ) );
}

void MainWindow::on_X_EditBox_textChanged(const QString &arg1)
{
    QString letter = "X";
    on_EditBox_textChanged( (letter + arg1 ) );
}

void MainWindow::on_Y_EditBox_textChanged(const QString &arg1)
{
    QString letter = "Y";
    on_EditBox_textChanged( (letter + arg1 ) );
}

void MainWindow::on_Z_EditBox_textChanged(const QString &arg1)
{
    QString letter = "Z";
    on_EditBox_textChanged( (letter + arg1 ) );
}








