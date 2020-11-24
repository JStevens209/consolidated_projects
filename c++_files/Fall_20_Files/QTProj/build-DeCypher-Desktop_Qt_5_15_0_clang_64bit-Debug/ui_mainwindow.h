/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 5.15.0
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenu>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QScrollArea>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QTableWidget>
#include <QtWidgets/QTextEdit>
#include <QtWidgets/QToolButton>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QAction *actionHelp;
    QAction *actionAbout;
    QWidget *centralwidget;
    QLabel *label_2;
    QWidget *layoutWidget;
    QHBoxLayout *horizontalLayout;
    QVBoxLayout *N_ZLayout;
    QLabel *N_Label;
    QLabel *O_Label;
    QLabel *P_Label;
    QLabel *Q_Label;
    QLabel *R_Label;
    QLabel *S_Label;
    QLabel *T_Label;
    QLabel *U_Label;
    QLabel *V_Label;
    QLabel *W_Label;
    QLabel *X_Label;
    QLabel *Y_Label;
    QLabel *Z_Label;
    QVBoxLayout *N_ZEditLayout;
    QLineEdit *N_EditBox;
    QLineEdit *O_EditBox;
    QLineEdit *P_EditBox;
    QLineEdit *Q_EditBox;
    QLineEdit *R_EditBox;
    QLineEdit *S_EditBox;
    QLineEdit *T_EditBox;
    QLineEdit *U_EditBox;
    QLineEdit *V_EditBox;
    QLineEdit *W_EditBox;
    QLineEdit *X_EditBox;
    QLineEdit *Y_EditBox;
    QLineEdit *Z_EditBox;
    QWidget *layoutWidget1;
    QHBoxLayout *horizontalLayout_2;
    QVBoxLayout *A_MLayout;
    QLabel *A_Label;
    QLabel *B_Label;
    QLabel *C_Label;
    QLabel *D_Label;
    QLabel *E_Label;
    QLabel *F_Label;
    QLabel *G_Label;
    QLabel *H_Label;
    QLabel *I_Label;
    QLabel *J_Label;
    QLabel *K_Label;
    QLabel *L_Label;
    QLabel *M_Label;
    QVBoxLayout *A_MEditLayout;
    QLineEdit *A_EditBox;
    QLineEdit *B_EditBox;
    QLineEdit *C_EditBox;
    QLineEdit *D_EditBox;
    QLineEdit *E_EditBox;
    QLineEdit *F_EditBox;
    QLineEdit *G_EditBox;
    QLineEdit *H_EditBox;
    QLineEdit *I_EditBox;
    QLineEdit *J_EditBox;
    QLineEdit *K_EditBox;
    QLineEdit *L_EditBox;
    QLineEdit *M_EditBox;
    QWidget *layoutWidget2;
    QVBoxLayout *verticalLayout_2;
    QLabel *label;
    QScrollArea *cipherArea;
    QWidget *scrollAreaWidgetContents;
    QTextEdit *cipherTextEdit;
    QLabel *label_3;
    QScrollArea *scrollArea;
    QWidget *scrollAreaWidgetContents_2;
    QTextEdit *plainTextEdit;
    QLineEdit *filePath;
    QPushButton *browseCipher;
    QLabel *label_30;
    QLabel *label_29;
    QWidget *layoutWidget3;
    QHBoxLayout *horizontalLayout_3;
    QPushButton *guess;
    QPushButton *calibrate;
    QToolButton *browse;
    QWidget *layoutWidget4;
    QHBoxLayout *horizontalLayout_4;
    QVBoxLayout *verticalLayout;
    QTableWidget *expectedFreq;
    QVBoxLayout *verticalLayout_3;
    QTableWidget *cipherFreq;
    QMenuBar *menubar;
    QMenu *menuDeCypher;
    QMenu *menuHelp;
    QStatusBar *statusbar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QString::fromUtf8("MainWindow"));
        MainWindow->resize(1565, 961);
        QPalette palette;
        QBrush brush(QColor(180, 189, 194, 216));
        brush.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::WindowText, brush);
        QBrush brush1(QColor(43, 42, 47, 255));
        brush1.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::Button, brush1);
        QBrush brush2(QColor(174, 183, 192, 255));
        brush2.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::Dark, brush2);
        QBrush brush3(QColor(33, 31, 36, 255));
        brush3.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::Mid, brush3);
        QBrush brush4(QColor(156, 153, 172, 216));
        brush4.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::Text, brush4);
        QBrush brush5(QColor(54, 54, 59, 255));
        brush5.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::BrightText, brush5);
        QBrush brush6(QColor(144, 147, 156, 255));
        brush6.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::ButtonText, brush6);
        QBrush brush7(QColor(31, 31, 32, 255));
        brush7.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::Base, brush7);
        QBrush brush8(QColor(45, 45, 46, 255));
        brush8.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::Window, brush8);
        QBrush brush9(QColor(52, 115, 207, 152));
        brush9.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::Highlight, brush9);
        QBrush brush10(QColor(227, 219, 255, 255));
        brush10.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::HighlightedText, brush10);
        QBrush brush11(QColor(152, 152, 152, 65));
        brush11.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::AlternateBase, brush11);
        QBrush brush12(QColor(156, 153, 172, 128));
        brush12.setStyle(Qt::SolidPattern);
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette::Active, QPalette::PlaceholderText, brush12);
#endif
        palette.setBrush(QPalette::Inactive, QPalette::WindowText, brush);
        palette.setBrush(QPalette::Inactive, QPalette::Button, brush1);
        palette.setBrush(QPalette::Inactive, QPalette::Dark, brush2);
        palette.setBrush(QPalette::Inactive, QPalette::Mid, brush3);
        palette.setBrush(QPalette::Inactive, QPalette::Text, brush4);
        palette.setBrush(QPalette::Inactive, QPalette::BrightText, brush5);
        palette.setBrush(QPalette::Inactive, QPalette::ButtonText, brush6);
        palette.setBrush(QPalette::Inactive, QPalette::Base, brush7);
        palette.setBrush(QPalette::Inactive, QPalette::Window, brush8);
        palette.setBrush(QPalette::Inactive, QPalette::Highlight, brush9);
        palette.setBrush(QPalette::Inactive, QPalette::HighlightedText, brush10);
        palette.setBrush(QPalette::Inactive, QPalette::AlternateBase, brush11);
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette::Inactive, QPalette::PlaceholderText, brush12);
#endif
        palette.setBrush(QPalette::Disabled, QPalette::WindowText, brush2);
        palette.setBrush(QPalette::Disabled, QPalette::Button, brush1);
        palette.setBrush(QPalette::Disabled, QPalette::Dark, brush2);
        palette.setBrush(QPalette::Disabled, QPalette::Mid, brush3);
        palette.setBrush(QPalette::Disabled, QPalette::Text, brush2);
        palette.setBrush(QPalette::Disabled, QPalette::BrightText, brush5);
        palette.setBrush(QPalette::Disabled, QPalette::ButtonText, brush2);
        palette.setBrush(QPalette::Disabled, QPalette::Base, brush8);
        palette.setBrush(QPalette::Disabled, QPalette::Window, brush8);
        QBrush brush13(QColor(70, 70, 70, 255));
        brush13.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Disabled, QPalette::Highlight, brush13);
        palette.setBrush(QPalette::Disabled, QPalette::HighlightedText, brush10);
        palette.setBrush(QPalette::Disabled, QPalette::AlternateBase, brush11);
        QBrush brush14(QColor(255, 255, 255, 128));
        brush14.setStyle(Qt::SolidPattern);
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette::Disabled, QPalette::PlaceholderText, brush14);
#endif
        MainWindow->setPalette(palette);
        actionHelp = new QAction(MainWindow);
        actionHelp->setObjectName(QString::fromUtf8("actionHelp"));
        QFont font;
        font.setFamily(QString::fromUtf8("Helvetica"));
        actionHelp->setFont(font);
        actionAbout = new QAction(MainWindow);
        actionAbout->setObjectName(QString::fromUtf8("actionAbout"));
        actionAbout->setFont(font);
        centralwidget = new QWidget(MainWindow);
        centralwidget->setObjectName(QString::fromUtf8("centralwidget"));
        label_2 = new QLabel(centralwidget);
        label_2->setObjectName(QString::fromUtf8("label_2"));
        label_2->setGeometry(QRect(30, 50, 151, 16));
        QFont font1;
        font1.setFamily(QString::fromUtf8("Helvetica"));
        font1.setBold(true);
        font1.setWeight(75);
        label_2->setFont(font1);
        layoutWidget = new QWidget(centralwidget);
        layoutWidget->setObjectName(QString::fromUtf8("layoutWidget"));
        layoutWidget->setGeometry(QRect(130, 80, 51, 531));
        horizontalLayout = new QHBoxLayout(layoutWidget);
        horizontalLayout->setSpacing(4);
        horizontalLayout->setObjectName(QString::fromUtf8("horizontalLayout"));
        horizontalLayout->setContentsMargins(0, 0, 0, 0);
        N_ZLayout = new QVBoxLayout();
        N_ZLayout->setSpacing(14);
        N_ZLayout->setObjectName(QString::fromUtf8("N_ZLayout"));
        N_Label = new QLabel(layoutWidget);
        N_Label->setObjectName(QString::fromUtf8("N_Label"));
        N_Label->setFont(font);

        N_ZLayout->addWidget(N_Label);

        O_Label = new QLabel(layoutWidget);
        O_Label->setObjectName(QString::fromUtf8("O_Label"));
        O_Label->setFont(font);

        N_ZLayout->addWidget(O_Label);

        P_Label = new QLabel(layoutWidget);
        P_Label->setObjectName(QString::fromUtf8("P_Label"));
        P_Label->setFont(font);

        N_ZLayout->addWidget(P_Label);

        Q_Label = new QLabel(layoutWidget);
        Q_Label->setObjectName(QString::fromUtf8("Q_Label"));
        Q_Label->setFont(font);

        N_ZLayout->addWidget(Q_Label);

        R_Label = new QLabel(layoutWidget);
        R_Label->setObjectName(QString::fromUtf8("R_Label"));
        R_Label->setFont(font);

        N_ZLayout->addWidget(R_Label);

        S_Label = new QLabel(layoutWidget);
        S_Label->setObjectName(QString::fromUtf8("S_Label"));
        S_Label->setFont(font);

        N_ZLayout->addWidget(S_Label);

        T_Label = new QLabel(layoutWidget);
        T_Label->setObjectName(QString::fromUtf8("T_Label"));
        T_Label->setFont(font);

        N_ZLayout->addWidget(T_Label);

        U_Label = new QLabel(layoutWidget);
        U_Label->setObjectName(QString::fromUtf8("U_Label"));
        U_Label->setFont(font);

        N_ZLayout->addWidget(U_Label);

        V_Label = new QLabel(layoutWidget);
        V_Label->setObjectName(QString::fromUtf8("V_Label"));
        V_Label->setFont(font);

        N_ZLayout->addWidget(V_Label);

        W_Label = new QLabel(layoutWidget);
        W_Label->setObjectName(QString::fromUtf8("W_Label"));
        W_Label->setFont(font);

        N_ZLayout->addWidget(W_Label);

        X_Label = new QLabel(layoutWidget);
        X_Label->setObjectName(QString::fromUtf8("X_Label"));
        X_Label->setFont(font);

        N_ZLayout->addWidget(X_Label);

        Y_Label = new QLabel(layoutWidget);
        Y_Label->setObjectName(QString::fromUtf8("Y_Label"));
        Y_Label->setFont(font);

        N_ZLayout->addWidget(Y_Label);

        Z_Label = new QLabel(layoutWidget);
        Z_Label->setObjectName(QString::fromUtf8("Z_Label"));
        Z_Label->setFont(font);

        N_ZLayout->addWidget(Z_Label);


        horizontalLayout->addLayout(N_ZLayout);

        N_ZEditLayout = new QVBoxLayout();
        N_ZEditLayout->setSpacing(20);
        N_ZEditLayout->setObjectName(QString::fromUtf8("N_ZEditLayout"));
        N_EditBox = new QLineEdit(layoutWidget);
        N_EditBox->setObjectName(QString::fromUtf8("N_EditBox"));
        N_EditBox->setFont(font);
        N_EditBox->setLayoutDirection(Qt::LeftToRight);
        N_EditBox->setMaxLength(1);

        N_ZEditLayout->addWidget(N_EditBox);

        O_EditBox = new QLineEdit(layoutWidget);
        O_EditBox->setObjectName(QString::fromUtf8("O_EditBox"));
        O_EditBox->setFont(font);
        O_EditBox->setLayoutDirection(Qt::LeftToRight);
        O_EditBox->setMaxLength(1);

        N_ZEditLayout->addWidget(O_EditBox);

        P_EditBox = new QLineEdit(layoutWidget);
        P_EditBox->setObjectName(QString::fromUtf8("P_EditBox"));
        P_EditBox->setFont(font);
        P_EditBox->setLayoutDirection(Qt::LeftToRight);
        P_EditBox->setMaxLength(1);

        N_ZEditLayout->addWidget(P_EditBox);

        Q_EditBox = new QLineEdit(layoutWidget);
        Q_EditBox->setObjectName(QString::fromUtf8("Q_EditBox"));
        Q_EditBox->setFont(font);
        Q_EditBox->setLayoutDirection(Qt::LeftToRight);
        Q_EditBox->setMaxLength(1);

        N_ZEditLayout->addWidget(Q_EditBox);

        R_EditBox = new QLineEdit(layoutWidget);
        R_EditBox->setObjectName(QString::fromUtf8("R_EditBox"));
        R_EditBox->setFont(font);
        R_EditBox->setLayoutDirection(Qt::LeftToRight);
        R_EditBox->setMaxLength(1);

        N_ZEditLayout->addWidget(R_EditBox);

        S_EditBox = new QLineEdit(layoutWidget);
        S_EditBox->setObjectName(QString::fromUtf8("S_EditBox"));
        S_EditBox->setFont(font);
        S_EditBox->setLayoutDirection(Qt::LeftToRight);
        S_EditBox->setMaxLength(1);

        N_ZEditLayout->addWidget(S_EditBox);

        T_EditBox = new QLineEdit(layoutWidget);
        T_EditBox->setObjectName(QString::fromUtf8("T_EditBox"));
        T_EditBox->setFont(font);
        T_EditBox->setLayoutDirection(Qt::LeftToRight);
        T_EditBox->setMaxLength(1);

        N_ZEditLayout->addWidget(T_EditBox);

        U_EditBox = new QLineEdit(layoutWidget);
        U_EditBox->setObjectName(QString::fromUtf8("U_EditBox"));
        U_EditBox->setFont(font);
        U_EditBox->setLayoutDirection(Qt::LeftToRight);
        U_EditBox->setMaxLength(1);

        N_ZEditLayout->addWidget(U_EditBox);

        V_EditBox = new QLineEdit(layoutWidget);
        V_EditBox->setObjectName(QString::fromUtf8("V_EditBox"));
        V_EditBox->setFont(font);
        V_EditBox->setLayoutDirection(Qt::LeftToRight);
        V_EditBox->setMaxLength(1);

        N_ZEditLayout->addWidget(V_EditBox);

        W_EditBox = new QLineEdit(layoutWidget);
        W_EditBox->setObjectName(QString::fromUtf8("W_EditBox"));
        W_EditBox->setFont(font);
        W_EditBox->setLayoutDirection(Qt::LeftToRight);
        W_EditBox->setMaxLength(1);

        N_ZEditLayout->addWidget(W_EditBox);

        X_EditBox = new QLineEdit(layoutWidget);
        X_EditBox->setObjectName(QString::fromUtf8("X_EditBox"));
        X_EditBox->setFont(font);
        X_EditBox->setLayoutDirection(Qt::LeftToRight);
        X_EditBox->setMaxLength(1);

        N_ZEditLayout->addWidget(X_EditBox);

        Y_EditBox = new QLineEdit(layoutWidget);
        Y_EditBox->setObjectName(QString::fromUtf8("Y_EditBox"));
        Y_EditBox->setFont(font);
        Y_EditBox->setLayoutDirection(Qt::LeftToRight);
        Y_EditBox->setMaxLength(1);

        N_ZEditLayout->addWidget(Y_EditBox);

        Z_EditBox = new QLineEdit(layoutWidget);
        Z_EditBox->setObjectName(QString::fromUtf8("Z_EditBox"));
        Z_EditBox->setFont(font);
        Z_EditBox->setLayoutDirection(Qt::LeftToRight);
        Z_EditBox->setMaxLength(1);

        N_ZEditLayout->addWidget(Z_EditBox);


        horizontalLayout->addLayout(N_ZEditLayout);

        layoutWidget1 = new QWidget(centralwidget);
        layoutWidget1->setObjectName(QString::fromUtf8("layoutWidget1"));
        layoutWidget1->setGeometry(QRect(50, 80, 51, 530));
        horizontalLayout_2 = new QHBoxLayout(layoutWidget1);
        horizontalLayout_2->setSpacing(4);
        horizontalLayout_2->setObjectName(QString::fromUtf8("horizontalLayout_2"));
        horizontalLayout_2->setContentsMargins(0, 0, 0, 0);
        A_MLayout = new QVBoxLayout();
        A_MLayout->setSpacing(14);
        A_MLayout->setObjectName(QString::fromUtf8("A_MLayout"));
        A_Label = new QLabel(layoutWidget1);
        A_Label->setObjectName(QString::fromUtf8("A_Label"));
        A_Label->setFont(font);

        A_MLayout->addWidget(A_Label);

        B_Label = new QLabel(layoutWidget1);
        B_Label->setObjectName(QString::fromUtf8("B_Label"));
        B_Label->setFont(font);

        A_MLayout->addWidget(B_Label);

        C_Label = new QLabel(layoutWidget1);
        C_Label->setObjectName(QString::fromUtf8("C_Label"));
        C_Label->setFont(font);

        A_MLayout->addWidget(C_Label);

        D_Label = new QLabel(layoutWidget1);
        D_Label->setObjectName(QString::fromUtf8("D_Label"));
        D_Label->setFont(font);

        A_MLayout->addWidget(D_Label);

        E_Label = new QLabel(layoutWidget1);
        E_Label->setObjectName(QString::fromUtf8("E_Label"));
        E_Label->setFont(font);

        A_MLayout->addWidget(E_Label);

        F_Label = new QLabel(layoutWidget1);
        F_Label->setObjectName(QString::fromUtf8("F_Label"));
        F_Label->setFont(font);

        A_MLayout->addWidget(F_Label);

        G_Label = new QLabel(layoutWidget1);
        G_Label->setObjectName(QString::fromUtf8("G_Label"));
        G_Label->setFont(font);

        A_MLayout->addWidget(G_Label);

        H_Label = new QLabel(layoutWidget1);
        H_Label->setObjectName(QString::fromUtf8("H_Label"));
        H_Label->setFont(font);

        A_MLayout->addWidget(H_Label);

        I_Label = new QLabel(layoutWidget1);
        I_Label->setObjectName(QString::fromUtf8("I_Label"));
        I_Label->setFont(font);

        A_MLayout->addWidget(I_Label);

        J_Label = new QLabel(layoutWidget1);
        J_Label->setObjectName(QString::fromUtf8("J_Label"));
        J_Label->setFont(font);

        A_MLayout->addWidget(J_Label);

        K_Label = new QLabel(layoutWidget1);
        K_Label->setObjectName(QString::fromUtf8("K_Label"));
        K_Label->setFont(font);

        A_MLayout->addWidget(K_Label);

        L_Label = new QLabel(layoutWidget1);
        L_Label->setObjectName(QString::fromUtf8("L_Label"));
        L_Label->setFont(font);

        A_MLayout->addWidget(L_Label);

        M_Label = new QLabel(layoutWidget1);
        M_Label->setObjectName(QString::fromUtf8("M_Label"));
        M_Label->setFont(font);

        A_MLayout->addWidget(M_Label);


        horizontalLayout_2->addLayout(A_MLayout);

        A_MEditLayout = new QVBoxLayout();
        A_MEditLayout->setSpacing(20);
        A_MEditLayout->setObjectName(QString::fromUtf8("A_MEditLayout"));
        A_EditBox = new QLineEdit(layoutWidget1);
        A_EditBox->setObjectName(QString::fromUtf8("A_EditBox"));
        A_EditBox->setFont(font);
        A_EditBox->setMaxLength(1);

        A_MEditLayout->addWidget(A_EditBox);

        B_EditBox = new QLineEdit(layoutWidget1);
        B_EditBox->setObjectName(QString::fromUtf8("B_EditBox"));
        B_EditBox->setFont(font);
        B_EditBox->setMaxLength(1);

        A_MEditLayout->addWidget(B_EditBox);

        C_EditBox = new QLineEdit(layoutWidget1);
        C_EditBox->setObjectName(QString::fromUtf8("C_EditBox"));
        C_EditBox->setFont(font);
        C_EditBox->setMaxLength(1);

        A_MEditLayout->addWidget(C_EditBox);

        D_EditBox = new QLineEdit(layoutWidget1);
        D_EditBox->setObjectName(QString::fromUtf8("D_EditBox"));
        D_EditBox->setFont(font);
        D_EditBox->setMaxLength(1);

        A_MEditLayout->addWidget(D_EditBox);

        E_EditBox = new QLineEdit(layoutWidget1);
        E_EditBox->setObjectName(QString::fromUtf8("E_EditBox"));
        E_EditBox->setFont(font);
        E_EditBox->setMaxLength(1);

        A_MEditLayout->addWidget(E_EditBox);

        F_EditBox = new QLineEdit(layoutWidget1);
        F_EditBox->setObjectName(QString::fromUtf8("F_EditBox"));
        F_EditBox->setFont(font);
        F_EditBox->setMaxLength(1);

        A_MEditLayout->addWidget(F_EditBox);

        G_EditBox = new QLineEdit(layoutWidget1);
        G_EditBox->setObjectName(QString::fromUtf8("G_EditBox"));
        G_EditBox->setFont(font);
        G_EditBox->setMaxLength(1);

        A_MEditLayout->addWidget(G_EditBox);

        H_EditBox = new QLineEdit(layoutWidget1);
        H_EditBox->setObjectName(QString::fromUtf8("H_EditBox"));
        H_EditBox->setFont(font);
        H_EditBox->setMaxLength(1);

        A_MEditLayout->addWidget(H_EditBox);

        I_EditBox = new QLineEdit(layoutWidget1);
        I_EditBox->setObjectName(QString::fromUtf8("I_EditBox"));
        I_EditBox->setFont(font);
        I_EditBox->setMaxLength(1);

        A_MEditLayout->addWidget(I_EditBox);

        J_EditBox = new QLineEdit(layoutWidget1);
        J_EditBox->setObjectName(QString::fromUtf8("J_EditBox"));
        J_EditBox->setFont(font);
        J_EditBox->setMaxLength(1);

        A_MEditLayout->addWidget(J_EditBox);

        K_EditBox = new QLineEdit(layoutWidget1);
        K_EditBox->setObjectName(QString::fromUtf8("K_EditBox"));
        K_EditBox->setFont(font);
        K_EditBox->setMaxLength(1);

        A_MEditLayout->addWidget(K_EditBox);

        L_EditBox = new QLineEdit(layoutWidget1);
        L_EditBox->setObjectName(QString::fromUtf8("L_EditBox"));
        L_EditBox->setFont(font);
        L_EditBox->setMaxLength(1);

        A_MEditLayout->addWidget(L_EditBox);

        M_EditBox = new QLineEdit(layoutWidget1);
        M_EditBox->setObjectName(QString::fromUtf8("M_EditBox"));
        M_EditBox->setFont(font);
        M_EditBox->setMaxLength(1);

        A_MEditLayout->addWidget(M_EditBox);


        horizontalLayout_2->addLayout(A_MEditLayout);

        layoutWidget2 = new QWidget(centralwidget);
        layoutWidget2->setObjectName(QString::fromUtf8("layoutWidget2"));
        layoutWidget2->setGeometry(QRect(200, 20, 771, 691));
        verticalLayout_2 = new QVBoxLayout(layoutWidget2);
        verticalLayout_2->setObjectName(QString::fromUtf8("verticalLayout_2"));
        verticalLayout_2->setContentsMargins(0, 0, 0, 0);
        label = new QLabel(layoutWidget2);
        label->setObjectName(QString::fromUtf8("label"));
        QPalette palette1;
        QBrush brush15(QColor(185, 180, 189, 217));
        brush15.setStyle(Qt::SolidPattern);
        palette1.setBrush(QPalette::Active, QPalette::WindowText, brush15);
        QBrush brush16(QColor(42, 41, 42, 255));
        brush16.setStyle(Qt::SolidPattern);
        palette1.setBrush(QPalette::Active, QPalette::Button, brush16);
        QBrush brush17(QColor(169, 170, 192, 255));
        brush17.setStyle(Qt::SolidPattern);
        palette1.setBrush(QPalette::Active, QPalette::Text, brush17);
        QBrush brush18(QColor(138, 139, 153, 255));
        brush18.setStyle(Qt::SolidPattern);
        palette1.setBrush(QPalette::Active, QPalette::ButtonText, brush18);
        QBrush brush19(QColor(86, 120, 172, 255));
        brush19.setStyle(Qt::SolidPattern);
        palette1.setBrush(QPalette::Active, QPalette::Highlight, brush19);
        QBrush brush20(QColor(51, 123, 201, 255));
        brush20.setStyle(Qt::SolidPattern);
        palette1.setBrush(QPalette::Active, QPalette::Link, brush20);
        QBrush brush21(QColor(14, 51, 96, 255));
        brush21.setStyle(Qt::SolidPattern);
        palette1.setBrush(QPalette::Active, QPalette::LinkVisited, brush21);
        QBrush brush22(QColor(169, 170, 192, 128));
        brush22.setStyle(Qt::SolidPattern);
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette::Active, QPalette::PlaceholderText, brush22);
#endif
        palette1.setBrush(QPalette::Inactive, QPalette::WindowText, brush15);
        palette1.setBrush(QPalette::Inactive, QPalette::Button, brush16);
        palette1.setBrush(QPalette::Inactive, QPalette::Text, brush17);
        palette1.setBrush(QPalette::Inactive, QPalette::ButtonText, brush18);
        palette1.setBrush(QPalette::Inactive, QPalette::Highlight, brush19);
        palette1.setBrush(QPalette::Inactive, QPalette::Link, brush20);
        palette1.setBrush(QPalette::Inactive, QPalette::LinkVisited, brush21);
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette::Inactive, QPalette::PlaceholderText, brush22);
#endif
        QBrush brush23(QColor(255, 255, 255, 63));
        brush23.setStyle(Qt::SolidPattern);
        palette1.setBrush(QPalette::Disabled, QPalette::WindowText, brush23);
        palette1.setBrush(QPalette::Disabled, QPalette::Button, brush16);
        palette1.setBrush(QPalette::Disabled, QPalette::Text, brush23);
        QBrush brush24(QColor(31, 31, 31, 255));
        brush24.setStyle(Qt::SolidPattern);
        palette1.setBrush(QPalette::Disabled, QPalette::ButtonText, brush24);
        palette1.setBrush(QPalette::Disabled, QPalette::Highlight, brush13);
        palette1.setBrush(QPalette::Disabled, QPalette::Link, brush20);
        palette1.setBrush(QPalette::Disabled, QPalette::LinkVisited, brush21);
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette::Disabled, QPalette::PlaceholderText, brush14);
#endif
        label->setPalette(palette1);
        QFont font2;
        font2.setFamily(QString::fromUtf8("Helvetica"));
        font2.setPointSize(20);
        font2.setBold(true);
        font2.setWeight(75);
        label->setFont(font2);

        verticalLayout_2->addWidget(label);

        cipherArea = new QScrollArea(layoutWidget2);
        cipherArea->setObjectName(QString::fromUtf8("cipherArea"));
        cipherArea->setLayoutDirection(Qt::LeftToRight);
        cipherArea->setWidgetResizable(true);
        scrollAreaWidgetContents = new QWidget();
        scrollAreaWidgetContents->setObjectName(QString::fromUtf8("scrollAreaWidgetContents"));
        scrollAreaWidgetContents->setGeometry(QRect(0, 0, 767, 314));
        cipherTextEdit = new QTextEdit(scrollAreaWidgetContents);
        cipherTextEdit->setObjectName(QString::fromUtf8("cipherTextEdit"));
        cipherTextEdit->setGeometry(QRect(0, 0, 771, 311));
        cipherTextEdit->setFont(font);
        cipherTextEdit->setInputMethodHints(Qt::ImhDigitsOnly|Qt::ImhMultiLine);
        cipherTextEdit->setSizeAdjustPolicy(QAbstractScrollArea::AdjustToContents);
        cipherArea->setWidget(scrollAreaWidgetContents);

        verticalLayout_2->addWidget(cipherArea);

        label_3 = new QLabel(layoutWidget2);
        label_3->setObjectName(QString::fromUtf8("label_3"));
        QPalette palette2;
        palette2.setBrush(QPalette::Active, QPalette::WindowText, brush15);
        palette2.setBrush(QPalette::Active, QPalette::Button, brush16);
        palette2.setBrush(QPalette::Active, QPalette::Text, brush17);
        palette2.setBrush(QPalette::Active, QPalette::ButtonText, brush18);
        palette2.setBrush(QPalette::Active, QPalette::Highlight, brush19);
        palette2.setBrush(QPalette::Active, QPalette::Link, brush20);
        palette2.setBrush(QPalette::Active, QPalette::LinkVisited, brush21);
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette2.setBrush(QPalette::Active, QPalette::PlaceholderText, brush22);
#endif
        palette2.setBrush(QPalette::Inactive, QPalette::WindowText, brush15);
        palette2.setBrush(QPalette::Inactive, QPalette::Button, brush16);
        palette2.setBrush(QPalette::Inactive, QPalette::Text, brush17);
        palette2.setBrush(QPalette::Inactive, QPalette::ButtonText, brush18);
        palette2.setBrush(QPalette::Inactive, QPalette::Highlight, brush19);
        palette2.setBrush(QPalette::Inactive, QPalette::Link, brush20);
        palette2.setBrush(QPalette::Inactive, QPalette::LinkVisited, brush21);
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette2.setBrush(QPalette::Inactive, QPalette::PlaceholderText, brush22);
#endif
        palette2.setBrush(QPalette::Disabled, QPalette::WindowText, brush23);
        palette2.setBrush(QPalette::Disabled, QPalette::Button, brush16);
        palette2.setBrush(QPalette::Disabled, QPalette::Text, brush23);
        palette2.setBrush(QPalette::Disabled, QPalette::ButtonText, brush24);
        palette2.setBrush(QPalette::Disabled, QPalette::Highlight, brush13);
        palette2.setBrush(QPalette::Disabled, QPalette::Link, brush20);
        palette2.setBrush(QPalette::Disabled, QPalette::LinkVisited, brush21);
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette2.setBrush(QPalette::Disabled, QPalette::PlaceholderText, brush14);
#endif
        label_3->setPalette(palette2);
        label_3->setFont(font2);

        verticalLayout_2->addWidget(label_3);

        scrollArea = new QScrollArea(layoutWidget2);
        scrollArea->setObjectName(QString::fromUtf8("scrollArea"));
        scrollArea->setWidgetResizable(true);
        scrollAreaWidgetContents_2 = new QWidget();
        scrollAreaWidgetContents_2->setObjectName(QString::fromUtf8("scrollAreaWidgetContents_2"));
        scrollAreaWidgetContents_2->setGeometry(QRect(0, 0, 767, 313));
        plainTextEdit = new QTextEdit(scrollAreaWidgetContents_2);
        plainTextEdit->setObjectName(QString::fromUtf8("plainTextEdit"));
        plainTextEdit->setGeometry(QRect(3, -1, 771, 321));
        plainTextEdit->setFont(font);
        scrollArea->setWidget(scrollAreaWidgetContents_2);

        verticalLayout_2->addWidget(scrollArea);

        filePath = new QLineEdit(centralwidget);
        filePath->setObjectName(QString::fromUtf8("filePath"));
        filePath->setGeometry(QRect(1000, 690, 251, 22));
        filePath->setFont(font);
        browseCipher = new QPushButton(centralwidget);
        browseCipher->setObjectName(QString::fromUtf8("browseCipher"));
        browseCipher->setGeometry(QRect(110, 630, 80, 21));
        browseCipher->setFont(font);
        browseCipher->setLayoutDirection(Qt::LeftToRight);
        label_30 = new QLabel(centralwidget);
        label_30->setObjectName(QString::fromUtf8("label_30"));
        label_30->setGeometry(QRect(1210, 0, 171, 16));
        label_30->setFont(font1);
        label_29 = new QLabel(centralwidget);
        label_29->setObjectName(QString::fromUtf8("label_29"));
        label_29->setGeometry(QRect(1000, 0, 171, 16));
        label_29->setFont(font1);
        layoutWidget3 = new QWidget(centralwidget);
        layoutWidget3->setObjectName(QString::fromUtf8("layoutWidget3"));
        layoutWidget3->setGeometry(QRect(1000, 720, 198, 41));
        horizontalLayout_3 = new QHBoxLayout(layoutWidget3);
        horizontalLayout_3->setObjectName(QString::fromUtf8("horizontalLayout_3"));
        horizontalLayout_3->setContentsMargins(0, 0, 0, 0);
        guess = new QPushButton(layoutWidget3);
        guess->setObjectName(QString::fromUtf8("guess"));
        guess->setFont(font);
        guess->setLayoutDirection(Qt::LeftToRight);

        horizontalLayout_3->addWidget(guess);

        calibrate = new QPushButton(layoutWidget3);
        calibrate->setObjectName(QString::fromUtf8("calibrate"));
        calibrate->setFont(font);

        horizontalLayout_3->addWidget(calibrate);

        browse = new QToolButton(layoutWidget3);
        browse->setObjectName(QString::fromUtf8("browse"));

        horizontalLayout_3->addWidget(browse);

        layoutWidget4 = new QWidget(centralwidget);
        layoutWidget4->setObjectName(QString::fromUtf8("layoutWidget4"));
        layoutWidget4->setGeometry(QRect(1000, 20, 421, 661));
        horizontalLayout_4 = new QHBoxLayout(layoutWidget4);
        horizontalLayout_4->setObjectName(QString::fromUtf8("horizontalLayout_4"));
        horizontalLayout_4->setContentsMargins(0, 0, 0, 0);
        verticalLayout = new QVBoxLayout();
        verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
        expectedFreq = new QTableWidget(layoutWidget4);
        if (expectedFreq->columnCount() < 2)
            expectedFreq->setColumnCount(2);
        if (expectedFreq->rowCount() < 26)
            expectedFreq->setRowCount(26);
        expectedFreq->setObjectName(QString::fromUtf8("expectedFreq"));
        expectedFreq->setEnabled(true);
        expectedFreq->setFont(font);
        expectedFreq->setAutoFillBackground(false);
        expectedFreq->setShowGrid(true);
        expectedFreq->setRowCount(26);
        expectedFreq->setColumnCount(2);
        expectedFreq->horizontalHeader()->setVisible(false);
        expectedFreq->verticalHeader()->setVisible(false);
        expectedFreq->verticalHeader()->setDefaultSectionSize(25);
        expectedFreq->verticalHeader()->setHighlightSections(false);

        verticalLayout->addWidget(expectedFreq);


        horizontalLayout_4->addLayout(verticalLayout);

        verticalLayout_3 = new QVBoxLayout();
        verticalLayout_3->setObjectName(QString::fromUtf8("verticalLayout_3"));
        cipherFreq = new QTableWidget(layoutWidget4);
        if (cipherFreq->columnCount() < 2)
            cipherFreq->setColumnCount(2);
        if (cipherFreq->rowCount() < 26)
            cipherFreq->setRowCount(26);
        cipherFreq->setObjectName(QString::fromUtf8("cipherFreq"));
        cipherFreq->setEnabled(true);
        cipherFreq->setFont(font);
        cipherFreq->setAutoFillBackground(false);
        cipherFreq->setEditTriggers(QAbstractItemView::NoEditTriggers);
        cipherFreq->setTabKeyNavigation(true);
        cipherFreq->setProperty("showDropIndicator", QVariant(true));
        cipherFreq->setDragDropOverwriteMode(false);
        cipherFreq->setRowCount(26);
        cipherFreq->setColumnCount(2);
        cipherFreq->horizontalHeader()->setVisible(false);
        cipherFreq->verticalHeader()->setVisible(false);
        cipherFreq->verticalHeader()->setDefaultSectionSize(25);
        cipherFreq->verticalHeader()->setHighlightSections(false);

        verticalLayout_3->addWidget(cipherFreq);


        horizontalLayout_4->addLayout(verticalLayout_3);

        MainWindow->setCentralWidget(centralwidget);
        menubar = new QMenuBar(MainWindow);
        menubar->setObjectName(QString::fromUtf8("menubar"));
        menubar->setGeometry(QRect(0, 0, 1565, 22));
        menuDeCypher = new QMenu(menubar);
        menuDeCypher->setObjectName(QString::fromUtf8("menuDeCypher"));
        menuHelp = new QMenu(menubar);
        menuHelp->setObjectName(QString::fromUtf8("menuHelp"));
        MainWindow->setMenuBar(menubar);
        statusbar = new QStatusBar(MainWindow);
        statusbar->setObjectName(QString::fromUtf8("statusbar"));
        MainWindow->setStatusBar(statusbar);

        menubar->addAction(menuDeCypher->menuAction());
        menubar->addAction(menuHelp->menuAction());
        menuDeCypher->addSeparator();
        menuDeCypher->addSeparator();
        menuDeCypher->addAction(actionAbout);
        menuHelp->addAction(actionHelp);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QCoreApplication::translate("MainWindow", "MainWindow", nullptr));
        actionHelp->setText(QCoreApplication::translate("MainWindow", "Help", nullptr));
        actionAbout->setText(QCoreApplication::translate("MainWindow", "About", nullptr));
        label_2->setText(QCoreApplication::translate("MainWindow", "CipherText -> PlainText", nullptr));
        N_Label->setText(QCoreApplication::translate("MainWindow", "N", nullptr));
        O_Label->setText(QCoreApplication::translate("MainWindow", "O", nullptr));
        P_Label->setText(QCoreApplication::translate("MainWindow", "P", nullptr));
        Q_Label->setText(QCoreApplication::translate("MainWindow", "Q", nullptr));
        R_Label->setText(QCoreApplication::translate("MainWindow", "R", nullptr));
        S_Label->setText(QCoreApplication::translate("MainWindow", "S", nullptr));
        T_Label->setText(QCoreApplication::translate("MainWindow", "T", nullptr));
        U_Label->setText(QCoreApplication::translate("MainWindow", "U", nullptr));
        V_Label->setText(QCoreApplication::translate("MainWindow", "V", nullptr));
        W_Label->setText(QCoreApplication::translate("MainWindow", "W", nullptr));
        X_Label->setText(QCoreApplication::translate("MainWindow", "X", nullptr));
        Y_Label->setText(QCoreApplication::translate("MainWindow", "Y", nullptr));
        Z_Label->setText(QCoreApplication::translate("MainWindow", "Z", nullptr));
        A_Label->setText(QCoreApplication::translate("MainWindow", "A", nullptr));
        B_Label->setText(QCoreApplication::translate("MainWindow", "B", nullptr));
        C_Label->setText(QCoreApplication::translate("MainWindow", "C", nullptr));
        D_Label->setText(QCoreApplication::translate("MainWindow", "D", nullptr));
        E_Label->setText(QCoreApplication::translate("MainWindow", "E", nullptr));
        F_Label->setText(QCoreApplication::translate("MainWindow", "F", nullptr));
        G_Label->setText(QCoreApplication::translate("MainWindow", "G", nullptr));
        H_Label->setText(QCoreApplication::translate("MainWindow", "H", nullptr));
        I_Label->setText(QCoreApplication::translate("MainWindow", "I", nullptr));
        J_Label->setText(QCoreApplication::translate("MainWindow", "J", nullptr));
        K_Label->setText(QCoreApplication::translate("MainWindow", "K", nullptr));
        L_Label->setText(QCoreApplication::translate("MainWindow", "L", nullptr));
        M_Label->setText(QCoreApplication::translate("MainWindow", "M", nullptr));
        label->setText(QCoreApplication::translate("MainWindow", "CipherText", nullptr));
        cipherTextEdit->setPlaceholderText(QCoreApplication::translate("MainWindow", "Copy ciphertext here.", nullptr));
        label_3->setText(QCoreApplication::translate("MainWindow", "PlainText", nullptr));
        plainTextEdit->setPlaceholderText(QCoreApplication::translate("MainWindow", "Plaintext will be translated here.", nullptr));
        filePath->setPlaceholderText(QCoreApplication::translate("MainWindow", "sample text filepath", nullptr));
        browseCipher->setText(QCoreApplication::translate("MainWindow", "Browse...", nullptr));
        label_30->setText(QCoreApplication::translate("MainWindow", "CipherText Letter Freq.", nullptr));
        label_29->setText(QCoreApplication::translate("MainWindow", "Expected Letter Freq.", nullptr));
        guess->setText(QCoreApplication::translate("MainWindow", "Guess", nullptr));
#if QT_CONFIG(shortcut)
        guess->setShortcut(QCoreApplication::translate("MainWindow", "Return", nullptr));
#endif // QT_CONFIG(shortcut)
        calibrate->setText(QCoreApplication::translate("MainWindow", "Calibrate", nullptr));
        browse->setText(QCoreApplication::translate("MainWindow", "...", nullptr));
        menuDeCypher->setTitle(QCoreApplication::translate("MainWindow", "DeCypher", nullptr));
        menuHelp->setTitle(QCoreApplication::translate("MainWindow", "Help", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
