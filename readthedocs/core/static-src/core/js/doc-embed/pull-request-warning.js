function init(data) {

    var warning = document.createElement('div');
    warning.className = 'admonition warning';

    var title = document.createElement('p');
    title.className = 'admonition-title';
    title.innerText = 'Note';

    var content = document.createElement('p');

    var build_link = document.createElement('a');
    build_link.innerText = 'was created';
    build_link.href = 'https://google.com';

    var pr_link = document.createElement('a');
    pr_link.innerText = '#' + data.version_name;
    pr_link.href = data.vcs_url;

    var commit_link = document.createElement('a');
    commit_link.innerText = data.version_identifier;
    commit_link.href = 'https://google.com';

    content.append(
      document.createTextNode('This page '),
      build_link,
      document.createTextNode(' from a pull request '),
      pr_link,
      document.createTextNode(' / '),
      commit_link,
      document.createTextNode('.')
    );

    warning.append(title, content);

    var selectors = ['[role=main]', 'main'];
    for (var i = 0; i < selectors.length; i += 1) {
        var body = document.body.querySelector(selectors[i]);
        if (body) {
            body.prepend(warning);
            break;
        }
    }
}


module.exports = {
    init: init
};
