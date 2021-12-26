import fs from 'fs';
import path from 'path';
import Event from '../types/event';

const events: Event[] = [];

// get event files
const eventFiles: Array<Array<string>> = fs
  .readdirSync('./dist/src/events')
  .map((file: string) => path.join('./dist/src/events', file))
  .filter((file: string) => fs.lstatSync(file).isDirectory())
  .map((dir: string) =>
    fs
      .readdirSync(dir)
      .filter((file: string) => file.endsWith('.js'))
      .map((file: string) => path.join(dir, file))
  );

// load 'em in!
for (const filecol of eventFiles) {
  for (const name of filecol) {
    const event = require(`../../../${name}`); // eslint-disable-line @typescript-eslint/no-var-requires
    events.push(event.default);
  }
}

export default events;
