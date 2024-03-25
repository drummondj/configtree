var dagfuncs = window.dashAgGridFunctions = window.dashAgGridFunctions || {};


dagfuncs.getGroupNames = function (params) {
    let values = JSON.parse(document.getElementById("group-names-options").innerHTML);
    return { values: values };
}