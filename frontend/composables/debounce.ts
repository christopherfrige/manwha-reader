export function debounce(fn: Function, wait: number): (...args: any[]) => void {
    let timer: NodeJS.Timeout;

    return function(this: any, ...args: any[]): void {
        if (timer) {
            clearTimeout(timer); // clear any pre-existing timer
        }
        
        const context = this; // get the current context
        
        timer = setTimeout(() => {
            fn.apply(context, args); // call the function if time expires
        }, wait);
    };
}