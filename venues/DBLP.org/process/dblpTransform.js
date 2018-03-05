function (note) {
  var removeDigitsRegEx = /\s\d{4}$/;
	var et = require('elementtree');
	var XML = et.XML;
  var tree = new et.ElementTree(XML(note.content.dblp));

  // get the entity type
  var entityType = tree.getroot().tag;

  var titleElement = tree.find('./title');
  // DBLP likes to end titles with a period, strip that off.
  var title = titleElement.text.trim();

  // see if we have a modification date
  // if there is no mdate, user the 'year' field.
  var year = tree.find('./year');
  var dttm = Date.parse(tree.getroot().attrib.mdate + ' 00:00:00 GMT' || year.text);
  var key = tree.getroot().attrib.key;

  var json = {
    'entityType': entityType,
    'key': key
  };

  var _authors = tree.findall('./author');
  var authors = [];
  _authors.forEach( function (author) {
    authors.push(author.text.replace(removeDigitsRegEx, ''));
  });

  if (authors.length > 0) {
    json.authors = authors;
  }

  var _editors = tree.findall('./editor');
  var editors = [];
  _editors.forEach(function (editor) {
    editors.push(editor.text);
  });

  if (editors.length > 0) {
    json.editors = editors;
  }

  // get all tags in the entity
  tree.getroot()._children.forEach(function (rec) {
    if (rec.tag !== 'author' && rec.tag !== 'editor') {
      json[rec.tag] = rec.text;
    }

  });

  note.cdate = dttm;
  note.content = json;
  note.content.title = title;
	return note;
};
