export default interface MGEvent {
  name: string;
  once: boolean;
  execute(...args: any): void;
}
