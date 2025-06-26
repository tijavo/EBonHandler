const spreadsheetId = "1A812LiO5geOfTyClrs2ZTThbsiJcOsw3bFbepM584hk";


function addBill(bill,name,date ) {
    console.log("Adding bill: " + name);
    var spreadsheet = SpreadsheetApp.openById(spreadsheetId);
    var mainSheet = spreadsheet.getSheetByName("Main");
    var sum = 0;
    var count = 0;
    for (var i = 0; i < bill.length; i++) {
        let addition = parseFloat(bill[i][1].replace(",", "."));
        if (isNaN(addition)) {
            console.log("Skipping invalid value: " + bill[i][1]);
            continue; // Skip invalid values
        }
        sum += parseFloat(bill[i][1].replace(",", "."));
        count++;
    }
    if(spreadsheet.getSheetByName(name)) {
        var i = 2;
        while (spreadsheet.getSheetByName(name + " (" + i + ")")) {
            i++;
        }
        name = name + " (" + i + ")";
        console.log("Sheet with name already exists, renaming to " + name);
    }
    console.log("Adding bill to sheet: " + name + " with sum: " + sum + " and count: " + count);

    var sheet = spreadsheet.insertSheet(name);

    //hyperlink the new sheet to the main sheet
    
    mainSheet.appendRow([date,name, sum.toFixed(2), count, "=HYPERLINK(\"#gid=" + sheet.getSheetId() + "\", \"Zum Sheet\")"]);

    sheet.appendRow(["Artikel", "Preis", "Typ","Anzahl"]);
    for (var i = 0; i < bill.length; i++) {
        let article = bill[i][0];
        let price = parseFloat(bill[i][1].replace(",", "."));
        let type = bill[i][2];
        let count = parseFloat(bill[i][3].replace(",", "."));
        if (isNaN(price)) {
            console.log("Skipping invalid value: " + bill[i][1]);
            continue; // Skip invalid values
        }
        sheet.appendRow([article, price.toFixed(2), type,count.toFixed(2)]);
    }
    sheet.getRange(1, 1, 1, 3).setFontWeight("bold");
    sheet.getRange(1, 1, 1, 3).setBackground("#f0f0f0");
    sheet.getRange(1, 1, sheet.getLastRow(), 3).setNumberFormat("#,##0.00");
}


function checkForNewEmails() {
  const threads = GmailApp.search('is:unread has:attachment filename:pdf');

  threads.forEach(thread => {
    const messages = thread.getMessages();

    messages.forEach(message => {
      const author = message.getFrom();
      const subject = message.getSubject();
      if(author == 'REWE eBon <ebon@mailing.rewe.de>'){
        const attachments = message.getAttachments();
        attachments.forEach(attachment => {
          console.log(attachment.getContentType())
          if (attachment.getContentType() === 'application/octet-stream') {
            const payload = {
              'file': attachment.copyBlob()
            };

            const options = {
              method: 'post',
              payload: payload, // automatisch multipart/form-data
              muteHttpExceptions: true
            };

            var billName = subject;
            var date = '0';
            const datePattern = /(\d{1,2}\.\d{1,2}\.\d{4})/;
            const match = subject.match(datePattern);
            if (match) {
                billName = 'REWE' + match[1]; // '31.05.2025'
                date = match[1];
            }
            const response = UrlFetchApp.fetch('https://ebon.tijavo.com/upload-pdf', options);
            Logger.log(response.getContentText());
            if (response.getResponseCode() === 200) {
              console.log("PDF successfully uploaded");
              const jsonResponse = JSON.parse(response.getContentText());
              const bill = jsonResponse.data;
              if (bill && bill.length > 0) {
                console.log("Bill data received, adding to spreadsheet");
                addBill(bill, billName, date);
                message.markRead();  // Optional: als gelesen markieren
              } else {
                console.error("No bill data found in response");
              }
            } else {
              console.error("Error uploading PDF: " + response.getContentText());
            }

          }
        });
      }

    });

    //thread.markRead();  // Optional: ganze Konversation als gelesen markieren
  });
}

function markAllReweEmailsAsUnread() {
  const threads = GmailApp.search('from:"REWE eBon <ebon@mailing.rewe.de>"');
  threads.forEach(thread => {
    thread.markUnread();
  });
  console.log("All REWE emails marked as unread.");
}

function hideAllSheetsExceptMain() {
  const spreadsheet = SpreadsheetApp.openById(spreadsheetId);
  const sheets = spreadsheet.getSheets();
  sheets.forEach(sheet => {
    if (sheet.getName() !== "Main") {
      sheet.hideSheet();
    }
  });
  console.log("All sheets except 'Main' have been hidden.");
}

function mergeAllSheets(){
  const spreadsheet = SpreadsheetApp.openById(spreadsheetId);
  const mainSheet = spreadsheet.getSheetByName("Main");
  const newSheet = spreadsheet.insertSheet("Merged Bills");
  newSheet.appendRow(["Datum","Rechnung", "Name", "Preis" ]);

  const sheet_info = mainSheet.getRange(2, 1, mainSheet.getLastRow() - 1, 2).getValues();
  const mergedSheetData = [];

  sheet_info.forEach((info) => {
    const sheetName = info[1];
    const sheet = spreadsheet.getSheetByName(sheetName);
    if (sheet) {
      const data = sheet.getRange(2, 1, sheet.getLastRow() - 1, 3).getValues();
      data.forEach((row) => {
        mergedSheetData.push([info[0], sheetName, row[0], row[1]]);
      });
    }else{
      console.warn("Sheet not found: " + sheetName);
    }
  });

  if (mergedSheetData.length > 0) {
    newSheet.getRange(2, 1, mergedSheetData.length, mergedSheetData[0].length).setValues(mergedSheetData);
    console.log("All sheets merged into 'Merged Bills'.");
  } else {
    console.log("No data to merge.");
  }
}