#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

    QString cipherToPlaintextKeys[26][2] = {};


private slots:
    void on_browse_clicked();

    void on_browseCipher_clicked();

    void on_guess_clicked();

    void on_A_EditBox_textChanged(const QString &arg1);
    void on_B_EditBox_textChanged(const QString &arg1);
    void on_C_EditBox_textChanged(const QString &arg1);
    void on_D_EditBox_textChanged(const QString &arg1);
    void on_E_EditBox_textChanged(const QString &arg1);
    void on_F_EditBox_textChanged(const QString &arg1);
    void on_G_EditBox_textChanged(const QString &arg1);
    void on_H_EditBox_textChanged(const QString &arg1);
    void on_I_EditBox_textChanged(const QString &arg1);
    void on_J_EditBox_textChanged(const QString &arg1);
    void on_K_EditBox_textChanged(const QString &arg1);
    void on_L_EditBox_textChanged(const QString &arg1);
    void on_M_EditBox_textChanged(const QString &arg1);
    void on_N_EditBox_textChanged(const QString &arg1);
    void on_O_EditBox_textChanged(const QString &arg1);
    void on_P_EditBox_textChanged(const QString &arg1);
    void on_Q_EditBox_textChanged(const QString &arg1);
    void on_R_EditBox_textChanged(const QString &arg1);
    void on_S_EditBox_textChanged(const QString &arg1);
    void on_T_EditBox_textChanged(const QString &arg1);
    void on_U_EditBox_textChanged(const QString &arg1);
    void on_V_EditBox_textChanged(const QString &arg1);
    void on_W_EditBox_textChanged(const QString &arg1);
    void on_X_EditBox_textChanged(const QString &arg1);
    void on_Y_EditBox_textChanged(const QString &arg1);
    void on_Z_EditBox_textChanged(const QString &arg1);

    void on_calibrate_clicked();


private:
    Ui::MainWindow *ui;

    std::vector<std::vector<QString>> plaintextFreq;
    QString ciphertextFreq[26][2];

    void on_EditBox_textChanged(const QString &arg1);
    void get_cipherText_Freq();
    void updateFrequencyTables();

    void ptVectSet(QString l, QString n);
    void updatePlaintextFreq(const QString str = "", bool isDefault = true);

};
#endif // MAINWINDOW_H
