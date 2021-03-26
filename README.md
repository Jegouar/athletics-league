<h1>SCVAC League Western Division</h1>
<h3>Milestone Project 3 - Data Centric Development</h3>
<p>A web application for a local athletics league giving information about match venues and timetables.</p>
<h2>External user's goal</h2>
<p>For managers and athletes, to obtain up to date information about matches.</p>
<h2>Site owner's goal</h2>
<p>For organisers and officials, to share information with all participants rather than just the members of a mailing list.</p>
<h2>Features</h2>
<p>The initial focus of this project is general data about the league and matches:</p>
<ul>
<li>The participating clubs, with links to their own websites.</li>
<li>Match dates and venues with Google Maps.</li>
<li>Match timetables with events and age categories.</li>
</ul>
<p>All users can view the information presented on the site. 
Administrators and officials have a higher access level to enable new material to be added and existing material to be edited or deleted.</p>
<p>On opening the app, the SCVAC (Southern Counties Veterans Athletic Club) logo is drawn and a welcome message appears on a grass bakground.
Then the participating club names (with links to their websites) translate from the left in individual lanes of an athletics track.
The numbers worn by athletes for competition then appear.</p>
<p>Underneath the track, a navigation menu offers 'Matches', 'Declarations', 'Results', 'Log In' and 'Register'.
'Declarations' is not currently available but will be a feature of the app in future development.
The same applies for 'Results', so a link is provided to relevant meetings on the Power of 10 athletics database.</p>
<p>'Log In' and 'Register' display a form styled as a long jump pit.
Successful login or registration displays the user's profile page in a similar format.
The menu changes to show 'Profile' and Log Out', and the club names each show an editing button.</p>
<p>'Matches' takes the user to a differently styled page.
This has a brick wall background, brass plaque logo, title and navigation menu, and wood bars for each match.
When clicked the bar expands into a noticeboard with two sheets of paper, the first for general match details and a Google map, and the second for the timetable.</p>
<p>Users logged in with higher access see additional links to add, edit and delete:</p>
<ul>
<li>'Add match' bar above the existing match bars</li>
<li>'Edit match' Post-it note on the first sheet for editing the general match details.</li>
<li>'Edit the timetable' Post-it note on the second sheet for editing the timetable, or 'Add a timetable' if none has been created.</li>
<li>'Delete match' at the bottom of the noticeboard frame.</li>
</ul>
<p>The various 'add' and 'edit' pages are forms with the same styling as the 'Match' page.
'Add Match' and 'Edit Match' are single pages, while 'Add Timetable' and 'Edit Timetable' are multiple step forms covering all the events.</p>
<h2>Features for future development</h2>
<p>The work submitted for this project is to be expanded with additional functionality:</p>
<ul>
<li>The 'Declarations' page will enable team managers to declare athletes for their clubs. Then the declared athletes can be entered for specific events in a match timetable.</li>
<li>The 'Results' page will enable officials to enter positions and performances into forms pre-loaded with athlete details.</li>
<li>An additional search feature will enable quick retrieval of historical results and rankings.</li>
<li>An upload feature will enable users to share reports and photographs of specific events.</li>
<li>A notification feature to email or text user-specific messages.</li>
</ul>
<h2>Technologies and tools used</h2>
<ul>
<li>HTML5</li>
<li>CSS3</li>
<li>JavaScript</li>
<li>Python</li>
<li>Flask</li>
<li>MongoDB</li>
<li>SVG</li>
<li>Adobe Illustrator</li>
<li>Adobe Photoshop</li>
<li>Google Fonts</li>
<li>Google Maps</li>
<li>Github</li>
<li>Gitpod</li>
<li>Heroku</li>
</ul>
<h2>Planning and development</h2>
<p>This is a competition that I take part in myself as an athlete and team manager.
The inspiration for creating a web application for it came from the following:</p>
<ul>
<li>No mention of this division is given on the official SCVAC site.</li>
<li>Information is sent to the team managers of each club, who then have to pass it on to athletes.</li>
<li>Declarations and results are processed by means of Excel spreadsheets and emails.</li>
</ul>
<p>These factors lead to quite a laborious and slow process of administration.</p>
<h3>Design</h3>
<p>Looking at related websites reveals little in the way of creative graphics or even photography in many cases.
My aim was to incorporate some objects typically seen at an athletics track into the look of the site.</p>
<p>I like the distinctive SCVAC logo which is always a good place to start with 'branding'.
Unfortunately the only available copy of it was very low quality, measuring a little over 100 pixels wide.
This prompted me to draw a vector image using Adobe Illustrator, taking care to put strokes onto separate layers, adjust their directions appropriately and create distinct fill layers.
I then exported to SVG format and included it inline within the HTML file to enable straightforward CSS styling and animation.</p>
<p>The welcome, registration, login and profile pages should make it obvious that this is an athletics website, with the track and long jump pit being prominent.
On the matches pages a more flexible format was required, for which paper documents on a noticeboard was chosen.
This will also be the format for future developments on the site.</p>
<p>A disadvantage with creative styling is that certain useful form inputs such as a datepicker cannot be styled appropriately.
For this reason the 'Add Match' form uses dropdowns for weekday, date, month and year which is obviously not as user-friendly.</p>
<h3>Fonts</h3>
<p>The slab serif font used throughout the site is Roboto Slab, for it's readability at all sizes.
Other fonts are used to suit their positions or context:</p>
<ul>
<li>Allerta Stencil for the track.</li>
<li>Oswald for the numbers.</li>
<li>Rock Salt for the long jump pit</li>
<li>Special Elite for paper documentation.</li>
<li>Just Another Hand for paper form entries.</li>
<li>Permanent Marker for post-it notes.</li>
</ul>
<h2>Testing</h2>
<p>The unforgiving nature of Python+Flask meant that pages would not display unless coding was correct!</p>
<p>Testing of newly created features were carried out at as they were written and at each commit to Github.
The following browsers were used on a Windows PC:</p>
<ul>
<li>Google Chrome</li>
<li>Mozilla Firefox</li>
<li>Microsoft Edge</li>
<li>Opera</li>
<li>Internet Explorer</li>
</ul>
<p>Less frequent tests were also performed on an Android phone using Chrome and an iPhone and iMac using Safari.</p>
<p>To test the functionality of the site, various scenarios were played out for users with differing access rights and objectives.</p>
<h3>User without account or not logged in</h3>
<p><u>Step 1: Open Welcome page</u><br>
Expected outcome: Logo, welcome message, club and number animation sequence perform<em> - successful</em></p>
<p><u>Step 2: Test external links</u><br>
Expected outcome: External sites open in a new tab<em> - successful</em></p>
<p><u>Step 3: Open Matches page</u><br>
Expected outcome: Matches page displays correctly<em> - successful</em></p>
<p><u>Step 4: Open a match board</u><br>
Expected outcome: Match board opens and displays Google Map and timetable pages, aligned at random angles<em> - successful</em></p>
<h3>User without account</h3>
<p><u>Step 1: Open Register page</u><br>
Expected outcome: Register page displays correctly<em> - successful</em></p>
<p><u>Step 2: Attempt to register without required field</u><br>
Expected outcome: Alert to fill in appropriate field given and form not posted<em> - successful</em></p>
<p><u>Step 3: Attempt to register with all required fields entered</u><br>
Expected outcome: New user appears in database. Profile page displayed with welcome message<em> - successful</em></p>
<h3>User with account</h3>
<p><u>Step 1: Open Log In page</u><br>
Expected outcome: Log In page displays correctly<em> - successful</em></p>
<p><u>Step 2: Attempt to log in with incorrect details or without required field</u><br>
Expected outcome: Flash message and blank form displayed. User not logged in<em> - successful</em></p>
<p><u>Step 3: Attempt to log in with both fields entered correctly</u><br>
Expected outcome: Profile page displayed with welcome message<em> - successful</em></p>
<h3>User with higher access</h3>
<p><u>Step 1: Open Matches page</u><br>
Expected outcome: Matches page displays correctly with 'Add Match' bar displayed<em> - successful</em></p>
<p><u>Step 2: Open a match board</u><br>
Expected outcome: Match board opens and displays 'Edit match', 'Add a timetable' or 'Edit the timetable', and 'Delete match' links<em> - successful</em></p>
<p><u>Step 3: Attempt to add a match without all required fields</u><br>
Expected outcome: Form not sent<em> - successful</em></p>
<p><u>Step 4: Attempt to add a match with all fields entered correctly</u><br>
Expected outcome: New match appears in database. Matches page displayed with flash message<em> - successful</em></p>
<p><u>Step 5: Attempt to edit a match</u><br>
Expected outcome: Form loaded with existing values. Changes made in database. Matches page displayed with flash message<em> - successful</em></p>
<p><u>Step 6: Attempt to add a timetable</u><br>
Expected outcome: Form loaded with existing values. Changes made in database. Matches page displayed with flash message<em> - successful</em></p>


<h2>Deployment</h2>
<p>This site is hosted using GitHub pages, deployed directly from the master branch with the page name index.html to deploy correctly. 
The deployed site will update automatically upon new commits to the master branch.