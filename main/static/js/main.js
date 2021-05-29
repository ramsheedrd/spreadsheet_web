const openSheetDialogBtn = document.getElementById('create-sheet-btn')
const closeDialogBtn = document.getElementById('close-dialog')
const newSheetDialog = document.getElementById('new-sheet-dialog')
const newSheetTitleEl = document.getElementById('new-sheet-name')
const newSheetRowsEl = document.getElementById('new-sheet-rows')
const newSheetColsEl = document.getElementById('new-sheet-cols')
const newSheetID = document.getElementById('new-sheet-id')

function makeSheet(id, rows, cols, modify){
    const options = {
        mode: 'edit', // edit | read
        showToolbar: false,
        showGrid: true,
        showContextmenu: true,
        view: {
            height: () => document.documentElement.clientHeight-200,
            width: () =>  document.documentElement.clientWidth,
        },
        row: {
            len: parseInt(rows),
            height: 25,
        },
        col: {
            len: parseInt(cols),
            width: 100,
            indexWidth: 60,
            minWidth: 60,
        },
        style: {
            bgcolor: '#ffffff',
            align: 'left',
            valign: 'middle',
            textwrap: false,
            strike: false,
            underline: false,
            color: '#0a0a0a',
            font: {
            name: 'Helvetica',
            size: 10,
            bold: false,
            italic: false,
            },
        },
    }
    var sheet = x_spreadsheet('#sheet', options);   

    if(modify === true){
        // load data from db
        axios.get(`/load/${id}/`).then(resp => {
            sheet.loadData(JSON.parse(resp.data.data))
        });

    }

    sheet.change(data => {
        // save data to db
        axios.post('/save/', {
        sheetId: id,
        sheetData: JSON.stringify(sheet.getData())
        })
        .then(function (response) {
        })
        .catch(function (error) {
        console.log(error);
      });
    });
  

    document.querySelector('.x-spreadsheet-menu').style.display = 'none';

}

function openDialog(){
    newSheetDialog.style.display = 'block'
}

function closeDialog(){
    newSheetDialog.style.display = 'none'
}

openSheetDialogBtn.addEventListener('click', openDialog)
closeDialogBtn.addEventListener('click', closeDialog)



let title = newSheetTitleEl.value
let rows_count = newSheetRowsEl.value
let cols_count = newSheetColsEl.value



if(title && rows_count && cols_count && newSheetID.value){
    // creating a sheet
    id = parseInt(newSheetID.value)
    makeSheet(id, rows_count, cols_count)
}
else if(title && newSheetID.value){
    // modifying existing sheet
    id = parseInt(newSheetID.value)
    makeSheet(id, rows_count, cols_count, modify=true)
}



