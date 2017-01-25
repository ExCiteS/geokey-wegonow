/* ***********************************************
 * Changes the display of radio buttons for
 * contributing permissions on a project.
 *
 * Used in:
 * - projects/project_create.html
 * ***********************************************/

$(function() {
    'use strict';

    $('input[name="isprivate"]').change(function(event) {
        if ($(event.target).attr('id') === 'public') {
            $('.public').removeClass('hide');
            $('.private').addClass('hide');
        } else if ($(event.target).attr('id') === 'private') {
            $('.public').addClass('hide');
            $('.private').removeClass('hide');
        }
    });
});
